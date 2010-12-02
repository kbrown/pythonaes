#!/usr/bin/env python
"""
OFB Mode of operation

Running this file as __main__ will result in a self-test of the algorithm.

Algorithm per NIST SP 800-38A http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf

Copyright (c) 2010, Adam Newman http://www.caller9.com/
Licensed under the MIT license http://www.opensource.org/licenses/mit-license.php
"""
__author__ = "Adam Newman"

class OFBMode:
    """Perform OFB operation on a block and retain IV information for next operation"""
    def __init__(self, block_cipher, block_size):
        self._block_cipher = block_cipher
        self._block_size = block_size
        self._iv = [0] * block_size
        self.clear()
    
    def set_iv(self, iv):
        if (len(iv) == self._block_size):
            self._iv = iv
            self.clear()
    
    def clear(self):
        self._last_ciphertext = self._iv
    
    def encrypt_block(self, plaintext):
        cipher_iv = self._block_cipher.cipher_block(self._last_ciphertext)
        ciphertext = [i ^ j for i,j in zip (plaintext, cipher_iv)]
        self._last_ciphertext = cipher_iv
        return ciphertext
    
    def decrypt_block(self, ciphertext):
        cipher_iv = self._block_cipher.cipher_block(self._last_ciphertext)
        plaintext = [i ^ j for i,j in zip (cipher_iv, ciphertext)]
        self._last_ciphertext = cipher_iv
        return plaintext
        
if __name__ == "__main__":
    #Self test
    import key_expander
    import aes_cipher
    import test_keys
    
    test_data = test_keys.TestKeys()
    
    test_expander = key_expander.KeyExpander(256)
    test_expanded_key = test_expander.expand(test_data.test_mode_key)
    
    test_cipher = aes_cipher.AESCipher(test_expanded_key)
    
    test_ofb = OFBMode(test_cipher, 16)
    
    test_ofb.set_iv(test_data.test_mode_iv)    
    for k in range(4):
        print ('OFB encrypt test block', k, ':', end=' ')
        if (len([i for i, j in zip(test_data.test_ofb_ciphertext[k],test_ofb.encrypt_block(test_data.test_mode_plaintext[k])) if i == j]) == 16):
            print ('passed')
        else:
            print ('failed')
    
    test_ofb.set_iv(test_data.test_mode_iv)
    for k in range(4):
        print ('OFB decrypt test block', k, ':', end=' ')
        if (len([i for i, j in zip(test_data.test_mode_plaintext[k],test_ofb.decrypt_block(test_data.test_ofb_ciphertext[k])) if i == j]) == 16):
            print ('passed')
        else:
            print ('failed')