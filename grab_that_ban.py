#!/bin/python

#  ::::::::  :::::::::      :::     :::::::::        ::::::::::: :::    :::     ::: :::::::::::       :::::::::      :::     ::::    ::: ::::    ::: :::::::::: :::::::::  
# :+:    :+: :+:    :+:   :+: :+:   :+:    :+:           :+:     :+:    :+:   :+: :+:   :+:           :+:    :+:   :+: :+:   :+:+:   :+: :+:+:   :+: :+:        :+:    :+: 
# +:+        +:+    +:+  +:+   +:+  +:+    +:+           +:+     +:+    +:+  +:+   +:+  +:+           +:+    +:+  +:+   +:+  :+:+:+  +:+ :+:+:+  +:+ +:+        +:+    +:+ 
# :#:        +#++:++#:  +#++:++#++: +#++:++#+            +#+     +#++:++#++ +#++:++#++: +#+           +#++:++#+  +#++:++#++: +#+ +:+ +#+ +#+ +:+ +#+ +#++:++#   +#++:++#:  
# +#+   +#+# +#+    +#+ +#+     +#+ +#+    +#+           +#+     +#+    +#+ +#+     +#+ +#+           +#+    +#+ +#+     +#+ +#+  +#+#+# +#+  +#+#+# +#+        +#+    +#+ 
# #+#    #+# #+#    #+# #+#     #+# #+#    #+#           #+#     #+#    #+# #+#     #+# #+#           #+#    #+# #+#     #+# #+#   #+#+# #+#   #+#+# #+#        #+#    #+# 
#  ########  ###    ### ###     ### #########            ###     ###    ### ###     ### ###           #########  ###     ### ###    #### ###    #### ########## ###    ###                                                                                                                                                   
                                                                                                                                                
# Date created: 13/02/2026
# Last Revision: 13/02/2026

# Purpose: This script asks for a IP\Domain and a port (default is 80) and outputs information about it

import socket
import ssl
import sys

def grab_banner():
    # 1. Handle Arguments
    if len(sys.argv) < 2:
        # We print errors to 'stderr' so they don't end up inside your .txt file
        print("Usage: python3 grab_that_ban.py <domain> [port]", file=sys.stderr)
        sys.exit(1)
    
    target = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    hostname = target.replace("http://", "").replace("https://", "").split('/')[0]

    try:
        # 2. Connection Logic
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        if port == 443:
            context = ssl.create_default_context()
            s = context.wrap_socket(sock, server_hostname=hostname)
        else:
            s = sock

        s.connect((hostname, port))
        
        # 3. The Request
        request = f"HEAD / HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
        s.send(request.encode())
        
        # 4. The Output
        banner = s.recv(2048).decode('utf-8', errors='replace').strip()
        
        print(f"Results for {hostname}:{port}")
        print("-" * 30)
        print(banner, flush=True) 

    except Exception as e: # Error Handling
        print(f"Error connecting to {hostname}: {e}", file=sys.stderr)
    finally:
        try: s.close()
        except: pass

if __name__ == "__main__":
    grab_banner()
