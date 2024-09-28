(module
    (func $f1 (result i32)
        (block
            call 1
        )
        i32.const 1
    )
    (func $f2 (result i32)
        (block
            call 2
        )
        i32.const 2
    )
    (func $f3 (result i32)
        (block
            i32.const 3
        )
    )
)