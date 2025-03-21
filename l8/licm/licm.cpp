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
        errs() << "Inside a loop!\n";
        BasicBlock *preheader = L.getLoopPreheader();
        bool converged = false;
        while (!converged) {
            converged = true;
            std::list<Instruction *> loop_inv_instrs;
            // Iterate over the loop's blocks
            for (auto &BB : L.blocks()) {
                // Iterate over the block's instructions
                for (auto &I : *BB) {

                    if (!isa<BinaryOperator>(&I)) {
                        continue;   // Avoid more complicated instructions
                    }

                    bool defs_outside_loop = true;
                    for (auto &O: I.operands()) {
                        if (isa<Constant>(&O)) {
                            continue;
                        }
                        if (!L.contains(dyn_cast<Instruction>(&O)->getParent())) {
                            continue;
                        }
                        defs_outside_loop = false;
                    }

                    if (defs_outside_loop) {
                        loop_inv_instrs.push_back(&I);
                        converged = false;
                    }
                }
            }
            // Iterate through all loop invariant instructions and move them to preheader
            for (auto *I : loop_inv_instrs) {
                if (!isSafeToSpeculativelyExecute(I)) {
                    errs() << "Loop invariant instruction " << *I << " has side effects. Checking it dominates all exits"<< "\n";
                    SmallVector<BasicBlock *, 8> ExitBlocks;
                    auto DT = DominatorTree(*I->getParent()->getParent());
                    L.getExitBlocks(ExitBlocks);
                    bool dominates_exit_blocks = true;
                    for (auto &B : ExitBlocks) {
                        if (DT.dominates(I->getParent(), B)) {
                            dominates_exit_blocks = false;
                            break;
                        }
                    }
                    if (!dominates_exit_blocks) {
                        errs() << "Loop invariant instruction does not dominate all exits. Will not move to preheader.";
                        continue;
                    }
                }
                errs() << "Moving loop invariant instruction to preheader: " << *I << "\n";
                I->moveBefore(preheader->getTerminator());
            }
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
