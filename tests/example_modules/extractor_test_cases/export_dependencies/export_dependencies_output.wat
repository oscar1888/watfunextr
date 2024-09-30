(module
    (func $doit (param i32) (result i32)
        local.get 0
        i32.add
        call 1
    )
    (func $doit2 (param i32) (result i32)
        local.get 1
        i32.add
        call 2
    )
    (func $f4 (export "func4"))
    (export "func1" (func 0))
    (export "func1alias" (func 0))
    (export "func2" (func 1))
)