#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {

struct SkeletonPass : public PassInfoMixin<SkeletonPass> {
    PreservedAnalyses run(Module &M, ModuleAnalysisManager &AM) {
        // Loop over each function in a module
        for (auto &F : M) {
            errs() << "I saw a function called " << F.getName() << "!\n";

            // Loop over each basic block in a function
            for (auto &B : F) {

                // Loop over each instruction in a block 
                for (auto &I : B) {
                    // `dyn_cast<BinaryOperator<&I>` returns null if `I` is not a binop,
                    // and returns the same pointer if it actually is a binop
                    if (auto *BO = dyn_cast<BinaryOperator>(&I)) {

                        BO->print(errs());
                        errs() << "\n";

                        // Initialize LLVM's IRBuilder with the binary operator
                        IRBuilder<> builder(BO);

                        // extract the operands of the BO 
                        // Note: `getOperand` returns the pointer to the 
                        // instruction that actually produced the operand
                        Value* lhs = BO->getOperand(0);
                        Value* rhs = BO->getOperand(1);

                        // TODO: check if `rhs == 0` and add an if...else block
                        // to prevent division by 0 


                        // tell LLVM that none of the previous analyses were preserved
                        return PreservedAnalyses::none();

                    }

                }
            }
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
