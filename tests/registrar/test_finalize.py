

def test_finalize_name_to_label(registrar, mocker, fake_hash_hexout):
    mocker.patch('web3.Web3.sha3', side_effect=fake_hash_hexout)
    mocker.patch.object(registrar.core, 'finalizeAuction')
    registrar.finalize('theycallmetim.eth')
    expected_label_hash = '0x' + b'HASH(btheycallmetim)'.hex()
    registrar.core.finalizeAuction.assert_called_once_with(expected_label_hash,
                                                           transact={})
