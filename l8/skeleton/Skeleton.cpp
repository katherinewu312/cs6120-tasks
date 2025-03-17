#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {

struct SkeletonPass : public PassInfoMixin<SkeletonPass> {
    PreservedAnalyses run(Module &M, ModuleAnalysisManager &AM) {
        for (auto &F : M) {
            for (auto &B : F) {
                for (auto &I : B) {
                    // returns null if its not a binary operator,
                    // and returns the same pointer if it actually is a binary operator
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

                        lhs->print(errs());
                        errs() << "\n";
                        rhs->print(errs());
                        errs() << "\n";

                        // create a new multiply instruction w/ the same operands
                        // as above
                        Value* mul = builder.CreateMul(lhs, rhs);
                        mul->print(errs());
                        errs() << "\n";

                        // iterate over all the locations which use the instruction
                        for (auto &U : BO->uses()) {
                            User* user = U.getUser();
                            user->setOperand(U.getOperandNo(), mul);
                        }

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
