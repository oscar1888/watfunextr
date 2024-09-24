(module
    (func $a (param f32) (result i32)
        nop
    )
    (func (result i32)
        unreachable
    )
    (func $c (param f32) (result i32)
        nop
        unreachable
    )
)