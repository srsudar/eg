## config
Enable/Disable applications. The applications may be enabled and disabled independently over
different interfaces (USB and NFC). The configuration may also be protected by a lock code.

* Disable PIV over the NFC interface: `ykman config nfc --disable PIV`
* Enable all applications over USB: `ykman config usb --enable-all`
* Generate and set a random application lock code:: `ykman config set-lock-code --generate`

## fido
Manage FIDO applications.

* Reset the FIDO (FIDO2 and U2F) applications: `ykman fido reset`
* Change the FIDO2 PIN from 123456 to 654321:  
  `ykman fido set-pin --pin 123456 --new-pin 654321`

## mode
Manage connection modes (USB Interfaces). Get the current connection mode of the YubiKey, or set it to MODE.

* Set the OTP and FIDO mode: `ykman mode OTP+FIDO`
* Set the CCID only mode and use touch to eject the smart card:  
  `ykman mode CCID --touch-eject`

## oath
Manage OATH Application.

* Generate codes for credentials starting with 'yubi': `ykman oath code yubi`
* Add a touch credential with the secret key f5up4ub3dw and the name yubico:  
  `ykman oath add yubico f5up4ub3dw --touch`
* Set a password for the OATH application: `ykman oath set-password`

## openpgp
Manage OpenPGP Application.

* Set the retries for PIN, Reset Code and Admin PIN to 10:  
  `ykman openpgp set-retries 10 10 10`
* Require touch to use the authentication key: `ykman openpgp set-touch aut on`
* Export an OpenPGP certificate as PEM:  
  `ykman openpgp export-certificate <key> <certificate>`  
  (`<key>` is the slot to read from (sig, enc, aut, or att), `<certificate>` the file to write to)

## otp
Manage OTP Application. The YubiKey provides two keyboard-based slots which can each be configured with
a credential. Several credential types are supported.

A slot configuration may be write-protected with an access code. This prevents the configuration to be
overwritten without the access code provided. Mode switching the YubiKey is not possible when a slot is
configured with an access code.

* Swap the configurations between the two slots: `ykman otp swap`
* Program a random challenge-response credential to slot 2:  
  `ykman otp chalresp --generate 2`
* Program a Yubico OTP credential to slot 1, using the serial as public id:  
  `ykman otp yubiotp 1 --serial-public-id`
* Program a random 38 characters long static password to slot 2:  
  `ykman otp static --generate 2 --length 38`

## piv
Manage PIV Application.

* Generate an ECC P-256 private key and a self-signed certificate in slot 9a:  
  `ykman piv generate-key --algorithm ECCP256 9a pubkey.pem`  
  `ykman piv generate-certificate --subject "yubico" 9a pubkey.pem`
* Change the PIN from 123456 to 654321:  
  `ykman piv change-pin --pin 123456 --new-pin 654321`
* Reset all PIV data and restore default settings: `ykman piv reset`
