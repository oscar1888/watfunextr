(module
    ;; Returns n+1 if control >= 0, n-1 otherwise.
    (func $ifexpr (param $n i32) (param $control i32) (result i32)
        (i32.add
            (local.get $n)
            (if (result i32)
                (i32.ge_s (local.get $control) (i32.const 0))
                (then (i32.const 1))
                (else (i32.const -1))
            )
        )
    )
)