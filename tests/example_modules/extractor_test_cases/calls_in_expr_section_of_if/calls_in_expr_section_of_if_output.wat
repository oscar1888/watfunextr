(module
    (func $is_even (param $n i32) (result i32)
        (if (result i32)
            (i32.eqz (local.get $n) (call 1))
            (then
                (i32.const 1)
            )
            (else
                (i32.sub (local.get $n) (i32.const 1))
            )
        )
    )
    (func $is_odd (param $n i32) (result i32)
        (if (result i32)
            (i32.eqz (local.get $n) (call 0))
            (then
                (i32.const 0)
            )
            (else
                (i32.sub (local.get $n) (i32.const 1))
            )
        )
    )
)