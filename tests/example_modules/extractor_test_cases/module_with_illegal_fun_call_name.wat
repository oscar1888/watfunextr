(module
    (func (result i32)
        unreachable
    )
    (func $c (param f32) (result i32)
        call $add
        (return)
    )
)