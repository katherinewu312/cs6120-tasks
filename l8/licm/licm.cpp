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
    PreservedAnalyses run(Loop &L, LoopAnalysisManager &AM, LoopStandardAnalysisResults &AR, LPMUpdater &U) {
        // Iterate over the loop's blocks
        for (auto *BB : L.blocks()) {
            errs() << "Loop block: " << BB->getName() << "\n";
        }

        return PreservedAnalyses::none();
    }
};

}

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
  return {.APIVersion = LLVM_PLUGIN_API_VERSION,
          .PluginName = "LICM pass",
          .PluginVersion = "v0.2",
          .RegisterPassBuilderCallbacks = [](PassBuilder &PB) {
            PB.registerLoopOptimizerEndEPCallback(
                [](LoopPassManager &LPM, OptimizationLevel Level) {
                  LPM.addPass(LICMPass());
                });
          }};
}
