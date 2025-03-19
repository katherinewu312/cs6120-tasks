#include "llvm/Analysis/LoopInfo.h"
#include "llvm/Analysis/LoopPass.h"
#include "llvm/Analysis/MemorySSAUpdater.h"
#include "llvm/Analysis/ValueTracking.h"
#include "llvm/IR/Function.h"
#include "llvm/Pass.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Transforms/Utils/LoopUtils.h"

using namespace llvm;

namespace {

struct LICMPass : public PassInfoMixin<LICMPass> {
    // library functions to look at:
    // `Loop::hasLoopInvariantOperands`
    // `LoopBase::getLoopPreheader`
    // `Instruction::moveBefore`

    // other helpful functions:
    // `llvm::isSafeToSpeculativelyExecute`
    // `BasicBlock::getTerminator`

    PreservedAnalyses run(Loop &L, LoopAnalysisManager &AM, LoopStandardAnalysisResults &AR, LPMUpdater &U) {
        errs() << "Inside a loop!\n";
        BasicBlock *preheader = L.getLoopPreheader();
        std::list<Instruction *> loop_inv_instrs;
        // Iterate over the loop's blocks
        for (auto &BB : L.blocks()) {
            // Iterate over the block's instructions
            for (auto &I : *BB) {
                // Check if instruction is loop invariant and contains no side effects or undefined behavior
                if (L.hasLoopInvariantOperands(&I) && isSafeToSpeculativelyExecute(&I)) {
                    loop_inv_instrs.push_back(&I);
                }
            }
        }

        // Iterate through all loop invariant instructions and move them to preheader
        for (auto *I : loop_inv_instrs) {
            errs() << "Moving loop invariant instruction to preheader: " << *I << "\n";
            I->moveBefore(preheader->getTerminator());
        }

        return PreservedAnalyses::none();
    }
};

}

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
  return {.APIVersion = LLVM_PLUGIN_API_VERSION,
          .PluginName = "LICMPass",
          .PluginVersion = "v0.1",
          .RegisterPassBuilderCallbacks = [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
              [](StringRef name, FunctionPassManager &FPM,
                ArrayRef<PassBuilder::PipelineElement>) {
                if (name != "LICMPass") return false;
                FPM.addPass(createFunctionToLoopPassAdaptor(LICMPass()));
                return true;
              });
          }};
}
