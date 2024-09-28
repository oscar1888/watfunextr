(module
    (func $f1 (result i32)
        call $f2
        i32.const 1
    )

    (func $f2 (result i32)
        call $f1
        call $f2
        call $f3
        i32.const 2
    )

    (func $f3 (result i32)
        call $f3
        i32.const 3
    )
)