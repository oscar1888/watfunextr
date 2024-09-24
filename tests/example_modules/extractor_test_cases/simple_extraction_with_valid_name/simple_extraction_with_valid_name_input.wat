(module
    (func $a (param f32) (result i32)
        (i32.const 5)
    )
    (func $b (result i32)
        unreachable
    )
    (func (param f32) (result i32)
        (i32.add)
    )
)