# retornar dominios sin repetir y en orden alfabetico:

correos = {
    "serj@soad.com",
    "lenny@debito.com",
    "maicol@jordan.com",
    "antony@herrera.com",
}
print(sorted({correo.split("@")[1] for correo in correos}))

