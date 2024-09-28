(module
    (func $f1 (result i32)
        (block
            call $f2
        )
        i32.const 1
    )
    (func $f2 (result i32)
        (block
            call $f3
        )
        i32.const 2
    )
    (func $f3 (result i32)
        (block
            i32.const 3
        )
    )
    (func $f4 (result i32)
        call $f5
        i32.const 4
    )
    (func $f5 (result i32)
        i32.const 5
    )
)