import os
import lnurl
import hashlib
from ecdsa import SigningKey, SECP256k1
from base64 import urlsafe_b64decode

# Server-side generation of auth URL
def generate_auth_url(domain, tag="login", action="login"):
    # Generate random 32 bytes for k1
    k1 = hashlib.sha256(os.urandom(32)).hexdigest()
    
    # Construct the authentication URL
    auth_url = f"https://{domain}?tag={tag}&k1={k1}&action={action}"

    # Bech32 encode the LNURL
    lnurl_bech32 = lnurl.encode(auth_url)

    # Construct the full LNURL
    lightninglink = f"LIGHTNING:{lnurl_bech32}"
    
    return auth_url, k1, lightninglink

# Server-side verification of the signature
def verify_signature(k1, key, sig):
    # Decode the signature using urlsafe_b64decode
    sig = urlsafe_b64decode(sig)
    
    # Verify the signature using secp256k1
    vk = SigningKey.from_string(bytes.fromhex(key), curve=SECP256k1).verifying_key
    try:
        vk.verify(sig, bytes.fromhex(k1))
        return True
    except Exception as e:
        print(f"Signature verification failed: {str(e)}")
        return False

if __name__ == '__main__':
    # Example usage
    domain = "www.jargonspeak.com"
    auth_url, k1, lightninglink = generate_auth_url(domain)
    print(f"Generated auth URL: {auth_url}")
    print(lightninglink, len(lightninglink))
    import qrcode
    qrcode.make(lightninglink)

    # # GET Request Path from Wallet
    # <LNURL_hostname_and_path>?<LNURL_existing_query_parameters>&sig=<hex(sign(hexToBytes(k1), linkingPrivKey))>&key=<hex(linkingKey)>

    # # Simulate wallet interaction by signing k1 with linkingPrivKey
    # # TODO: Replace with the actual linkingPrivKey
    # linking_priv_key_hex = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    # signature_hex = urlsafe_b64encode(SigningKey.from_string(bytes.fromhex(linking_priv_key_hex), curve=SECP256k1).sign(bytes.fromhex(k1))).decode("utf-8")
    # verification_result = verify_signature(k1, linking_priv_key_hex, signature_hex)

    # if verification_result:
    #     print("Signature verification successful. Proceed with authentication.")
    # else:
    #     print("Signature verification failed. Authentication aborted.")