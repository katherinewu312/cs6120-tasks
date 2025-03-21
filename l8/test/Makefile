opt:
	@for file in *.c; do \
		`brew --prefix llvm`/bin/clang -S -emit-llvm -O0 -Xclang -disable-O0-optnone $${file} -o $${file}.ll; \
		`brew --prefix llvm`/bin/opt -passes=mem2reg $${file}.ll -S -o $${file}.ll1; \
		`brew --prefix llvm`/bin/opt -load-pass-plugin=../build/licm/LICMPass.dylib -passes='LICMPass' $${file}.ll1 -S > $${file}.ll2; \
	done
