(module
    (func $is_even (type 0)
        (if (result i32)
            (i32.eqz (local.get $n))
            (then
                (i32.const 1)
            )
            (else
                (call 1 (i32.sub (local.get $n) (i32.const 1)))
            )
        )
    )
    (func $is_odd (type 0)
        (if (result i32)
            (i32.eqz (local.get $n))
            (then
                (i32.const 0)
            )
            (else
                (call 0 (i32.sub (local.get $n) (i32.const 1)))
            )
        )
        call 2
    )
    (func $f1 (type 1)
        nop
    )
    (type $second (func (param i32) (result i32)))
    (type (func (param f32) (result f32)))
)