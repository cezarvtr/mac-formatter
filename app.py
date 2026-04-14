from flask import Flask, request, render_template
import ipaddress
import re

app = Flask(__name__)

def limpar_mac(mac):
    return re.sub(r'[^0-9A-Fa-f]', '', mac).upper()

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = ""

    if request.method == "POST":
        tipo = request.form.get("tipo")

        if tipo == "mac":
            mac = request.form.get("mac", "")
            clean = limpar_mac(mac)

            if len(clean) != 12:
                resultado = "MAC inválido"
            else:
                p = [clean[i:i+2] for i in range(0, 12, 2)]

                mac1 = ":".join(p)
                mac2 = "-".join(p)
                mac3 = ".".join([clean[i:i+4] for i in range(0, 12, 4)])
                mac4 = "-".join([clean[i:i+4] for i in range(0, 12, 4)])

                resultado = {
                    "macs": [mac1, mac2, mac3, mac4]
                }

        elif tipo == "ip":
            ip = request.form.get("ip", "")

            try:
                rede = ipaddress.ip_network(ip, strict=False)
                hosts = rede.num_addresses - 2 if rede.num_addresses > 2 else 0
                lista = list(rede.hosts())

                resultado = {
                    "network": rede.network_address,
                    "broadcast": rede.broadcast_address,
                    "mask": rede.netmask,
                    "wildcard": rede.hostmask,
                    "cidr": rede.prefixlen,
                    "hostmin": lista[0] if lista else "-",
                    "hostmax": lista[-1] if lista else "-",
                    "hosts": hosts
                }
            except:
                resultado = "IP inválido"

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
