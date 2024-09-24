(module
    (func $f1 (param f32) (result i32)
        nop
    )
    (func (result i32)
        unreachable
    )
    (func $c (param f32) (result i32)
        drop
        nop
        (return)
    )
)