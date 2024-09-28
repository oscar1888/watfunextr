(module
    (func $is_even (param $n i32) (result i32)
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
    (func $is_odd (param $n i32) (result i32)
        (if (result i32)
            (i32.eqz (local.get $n))
            (then
                (i32.const 0)
            )
            (else
                (call 0 (i32.sub (local.get $n) (i32.const 1)))
            )
        )
    )
)