(module
    (func $f1 (param f32) (result i32)
        nop
    )
    (func (result i32)
        unreachable
    )

    (func $d (param i32) (param i32)
        (i32.const 3)
        call 3
        nop
    )
    (func $c (param f32) (result i32)
        drop
        nop
        (return)
    )
)