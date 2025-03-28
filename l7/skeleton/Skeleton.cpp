#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {

struct SkeletonPass : public PassInfoMixin<SkeletonPass> {
    PreservedAnalyses run(Module &M, ModuleAnalysisManager &AM) {
        bool modified = false;
        // Loop over each function in a module
        for (auto &F : M.functions()) {
            errs() << "Function " << F.getName() << "!\n";
            // Loop over each basic block in a function
            for (auto &B : F) {
                // Loop over each instruction in a block 
                for (auto I = B.begin(); I != B.end(); ) {
                    Instruction &Inst = *I;
                    ++I;
                    // `dyn_cast<BinaryOperator<&I>` returns null if `I` is not a binop,
                    // and returns the same pointer if it actually is a binop
                    if (auto *BO = dyn_cast<BinaryOperator>(&Inst)) {
                        // Initialize LLVM's IRBuilder with the binary operator
                        // (this inserts at the point where the instruciton `BO` occurs)
                        IRBuilder<> builder(BO);                        

                        // extract the operands of the BO 
                        // Note: `getOperand` returns the pointer to the 
                        // instruction that actually produced the operand
                        Value* numerator = BO->getOperand(0);
                        Value* denominator = BO->getOperand(1);

                        Type* denom_ty = denominator->getType();

                        Constant* zero;
                        Value* cmp_eq;
                        Instruction* div_copy;

                        // Integer division
                        if (BO->getOpcode() == Instruction::SDiv || BO->getOpcode() == Instruction::UDiv) {
                            // Found a division instruction
                            errs() << "Found integer division: \n";
                            Inst.print(errs(), true);
                            errs() << "\n";

                            if (denom_ty->isIntegerTy()) {
                                // Create an integer comparison instruction
                                // which checks if the denominator is equal to 0
                                zero = ConstantInt::get(denom_ty, 0);
                                cmp_eq = builder.CreateICmpEQ(denominator, zero, "is_zero");
                            } else {
                                errs() << "we have an integer division but denominator doesn't have type int!\n";
                            }                                
                        } else if (BO->getOpcode() == Instruction::FDiv) {
                            // floating point division
                            errs() << "Found floating-point division : \n";
                            Inst.print(errs(), true);
                            errs() << "\n";

                            if (denom_ty->isFloatingPointTy()) {
                                // Create an floating point comparison instruction
                                // which checks if the denominator is equal to 0
                                zero = ConstantFP::get(denom_ty, 0);

                                // We use LLVM's *ordered equals* operator for FPs `FCmpOEQ`, 
                                // as opposed to `FCmpUEQ` (unordered equals), 
                                // since the former behaves more predictably with possibly null operands
                                cmp_eq = builder.CreateFCmpOEQ(denominator, zero, "is_zero");
                            } else {
                                errs() << "We have FP division but denominator doesn't have a floating point type!\n";
                            }
                        } else {
                            // Not a division
                            continue;
                        }

                        // Create a copy of the original division instruction
                        // (this will only be executed if the denominator is non-zero)
                        div_copy = BO->clone();
                        div_copy->setName(BO->getName() + "_copy");
                        builder.Insert(div_copy);

                        // Create a select instruction for safe division 
                        // (LLVM select instructions are akin to C's ternary operators)
                        // This means `cmp_eq ? zero : div_copy`
                        Value* safe_div_select = builder.CreateSelect(cmp_eq, zero, div_copy, "safe_div_result");
                        
                        errs() << "Created new instructions:\n";
                        cmp_eq->print(errs() , true);
                        errs() << "\n";
                        div_copy->print(errs() , true);
                        errs() << "\n";
                        safe_div_select->print(errs(), true);
                        errs() << "\n";

                        // Replace all uses of the original division instruction
                        // with the safe division instruction created above
                        for (auto &U : BO->uses()) {
                            // Fetch the entire instruction corresponding to the use
                            User *user = U.getUser();

                            errs() << "Original use:\n";
                            user->print(errs(), true);
                            errs() << "\n";

                            // Update the corresponding operand to use 
                            // the result of the safe division instead
                            user->setOperand(U.getOperandNo(), safe_div_select);

                            errs() << "Updated use:\n";
                            user->print(errs(), true);
                            errs() << "\n";
                        }

                        // Remove the original division instruction
                        BO->eraseFromParent();

                        // We modified the code
                        modified = true;
                    }
                }
            }
        }
        if (modified) {
            return PreservedAnalyses::none();
        }
        return PreservedAnalyses::all();
    };
};

}

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
    return {
        .APIVersion = LLVM_PLUGIN_API_VERSION,
        .PluginName = "Skeleton pass",
        .PluginVersion = "v0.1",
        .RegisterPassBuilderCallbacks = [](PassBuilder &PB) {
            PB.registerPipelineStartEPCallback(
                [](ModulePassManager &MPM, OptimizationLevel Level) {
                    MPM.addPass(SkeletonPass());
                });
        }
    };
}
