console.clear()
comm.socketServerSetIp("82.161.233.115")
comm.socketServerSetPort(32032)
print(comm.socketServerSend([[GET /game/list/LADXR HTTP/1.1
Host: daid.eu

]]))
received_data = ""

event.onframeend(function()
    local data = comm.socketServerResponse()
    if #data > 0 then
        received_data = received_data .. data
        local end_of_headers = received_data:find("\r\n\r\n")
        print(received_data:sub(0, end_of_headers))
    end
    -- print(comm.socketServerResponse())
end)
