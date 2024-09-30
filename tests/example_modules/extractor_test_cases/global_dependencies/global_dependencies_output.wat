(module
    (func $doit (param i32) (result i32)
        local.get 0
        global.get 0
        i32.add
        call 1
    )
    (func $doit2 (param i32) (result i32)
        local.get 1
        global.get 0
        i32.add
        global.get 1
    )
    (global $from_wasm i32 (i32.const 10))
    (global $from_wasm2 i32 (i32.const 20))
)