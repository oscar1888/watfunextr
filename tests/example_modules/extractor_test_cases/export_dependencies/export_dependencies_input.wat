(module
    (export "func1" (func 0))
    (func $doit (param i32) (result i32)
        local.get 0
        i32.add
        call $doit2
    )
    (export "func1alias" (func 0))
    (func $f3)
    (func $doit2 (param i32) (result i32)
        local.get 1
        i32.add
        call $f4
    )
    (func $f4 (export "func4"))
    (export "func2" (func 2))
    (export "func3" (func 1))
)