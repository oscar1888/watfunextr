(module
    (global $from_wasm i32 (i32.const 10))
    (func $doit (param i32) (result i32)
        local.get 0
        global.get $from_wasm
        i32.add
        call $doit2
    )
    (global $from_wasm2 i32 (i32.const 20))
    (func $doit2 (param i32) (result i32)
        local.get 1
        global.get 0
        i32.add
        global.get 1
    )
    (global $isolated i32)
)