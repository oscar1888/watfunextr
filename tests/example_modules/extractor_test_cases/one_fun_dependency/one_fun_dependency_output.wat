(module
    (func $d (param i32) (param i32)
        (i32.const 3)
        call 1
        nop
    )
    (func $c (param f32) (result i32)
        drop
        nop
        (return)
    )
)