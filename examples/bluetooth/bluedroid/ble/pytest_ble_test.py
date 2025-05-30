# SPDX-FileCopyrightText: 2022-2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: CC0-1.0
import os.path
from typing import Tuple

import pexpect
import pytest
from pytest_embedded import Dut
from pytest_embedded_idf.dut import IdfDut
from pytest_embedded_idf.utils import idf_parametrize
# Case 1: gatt client and gatt server test
# EXAMPLE_CI_ID=3


@pytest.mark.wifi_two_dut
@pytest.mark.parametrize(
    'count, app_path, config, erase_nvs',
    [
        (
            2,
            f'{os.path.join(os.path.dirname(__file__), "gatt_server")}|{os.path.join(os.path.dirname(__file__), "gatt_client")}',
            'name',
            'y',
        ),
    ],
    indirect=True,
)
@idf_parametrize(
    'target', ['esp32', 'esp32c3', 'esp32c6', 'esp32c5', 'esp32h2', 'esp32s3', 'esp32c61'], indirect=['target']
)
def test_gatt_func(app_path: str, dut: Tuple[IdfDut, IdfDut]) -> None:
    gatt_client = dut[1]
    gatt_server = dut[0]
    gatt_client_addr = (
        gatt_client.expect(r'Bluetooth MAC: (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})', timeout=30).group(1).decode('utf8')
    )
    gatt_server_addr = (
        gatt_server.expect(r'Bluetooth MAC: (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})', timeout=30).group(1).decode('utf8')
    )
    gatt_client.expect_exact('GATT client register, status 0', timeout=30)
    gatt_server.expect_exact('GATT server register, status 0', timeout=30)
    gatt_server.expect_exact('Advertising start successfully', timeout=30)
    gatt_client.expect_exact('Scanning start successfully', timeout=30)
    gatt_client.expect_exact(f'Connected, conn_id 0, remote {gatt_server_addr}', timeout=30)
    gatt_server.expect_exact(f'Connected, conn_id 0, remote {gatt_client_addr}', timeout=30)
    gatt_client.expect_exact('Connection params update, status 0', timeout=30)
    gatt_server.expect_exact('Connection params update, status 0', timeout=30)
    gatt_client.expect_exact('Service discover complete', timeout=30)
    gatt_client.expect_exact('Service search complete', timeout=30)
    gatt_client.expect_exact('MTU exchange, status 0, MTU 500', timeout=30)
    gatt_server.expect_exact('MTU exchange, MTU 500', timeout=30)
    gatt_server.expect_exact('Notification enable', timeout=30)
    gatt_client.expect_exact('Notification received', timeout=30)
    gatt_client_output = gatt_client.expect(pexpect.TIMEOUT, timeout=10)
    gatt_server_output = gatt_server.expect(pexpect.TIMEOUT, timeout=10)
    assert 'rst:' not in str(gatt_client_output) and 'boot:' not in str(gatt_client_output)
    assert 'rst:' not in str(gatt_server_output) and 'boot:' not in str(gatt_server_output)
    assert 'Disconnected' not in str(gatt_client_output)
    assert 'Disconnected' not in str(gatt_server_output)


# Case 2: gatt client and gatt server test for ESP32C2 26mhz xtal
# EXAMPLE_CI_ID=3
@pytest.mark.wifi_two_dut
@pytest.mark.xtal_26mhz
@pytest.mark.parametrize(
    'count, target, baud, app_path, config, erase_nvs',
    [
        (
            2,
            'esp32c2|esp32c2',
            '74880',
            f'{os.path.join(os.path.dirname(__file__), "gatt_server")}|{os.path.join(os.path.dirname(__file__), "gatt_client")}',
            'esp32c2_xtal26m',
            'y',
        ),
    ],
    indirect=True,
)
def test_c2_26mhz_xtal_gatt_func(app_path: str, dut: Tuple[IdfDut, IdfDut]) -> None:
    gatt_client = dut[1]
    gatt_server = dut[0]
    gatt_client_addr = (
        gatt_client.expect(r'Bluetooth MAC: (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})').group(1).decode('utf8')
    )
    gatt_server_addr = (
        gatt_server.expect(r'Bluetooth MAC: (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})').group(1).decode('utf8')
    )
    gatt_client.expect_exact('GATT client register, status 0', timeout=30)
    gatt_server.expect_exact('GATT server register, status 0', timeout=30)
    gatt_server.expect_exact('Advertising start successfully', timeout=30)
    gatt_client.expect_exact('Scanning start success', timeout=30)
    gatt_client.expect_exact(f'Connected, conn_id 0, remote {gatt_server_addr}', timeout=30)
    gatt_server.expect_exact(f'Connected, conn_id 0, remote {gatt_client_addr}', timeout=30)
    gatt_client.expect_exact('Connection params update, status 0', timeout=30)
    gatt_server.expect_exact('Connection params update, status 0', timeout=30)
    gatt_client.expect_exact('Service discover complete', timeout=30)
    gatt_client.expect_exact('Service search complete', timeout=30)
    gatt_client.expect_exact('MTU exchange, status 0, MTU 500', timeout=30)
    gatt_server.expect_exact('MTU exchange, MTU 500', timeout=30)
    gatt_server.expect_exact('Notification enable', timeout=30)
    gatt_client.expect_exact('Notification received', timeout=30)
    gatt_client_output = gatt_client.expect(pexpect.TIMEOUT, timeout=10)
    gatt_server_output = gatt_server.expect(pexpect.TIMEOUT, timeout=10)
    assert 'rst:' not in str(gatt_client_output) and 'boot:' not in str(gatt_client_output)
    assert 'rst:' not in str(gatt_server_output) and 'boot:' not in str(gatt_server_output)
    assert 'Disconnected' not in str(gatt_client_output)
    assert 'Disconnected' not in str(gatt_server_output)


# Case 3: gatt security server and gatt security client test
# EXAMPLE_CI_ID=5
@pytest.mark.wifi_two_dut
@pytest.mark.parametrize(
    'count, app_path, config, erase_nvs',
    [
        (
            2,
            f'{os.path.join(os.path.dirname(__file__), "gatt_security_server")}|{os.path.join(os.path.dirname(__file__), "gatt_security_client")}',
            'name',
            'y',
        ),
    ],
    indirect=True,
)
@idf_parametrize(
    'target', ['esp32', 'esp32c3', 'esp32c6', 'esp32c5', 'esp32h2', 'esp32s3', 'esp32c61'], indirect=['target']
)
def test_gatt_security_func(app_path: str, dut: Tuple[IdfDut, IdfDut], target: Tuple) -> None:
    gatt_security_client = dut[1]
    gatt_security_server = dut[0]
    gatt_security_client_addr = (
        gatt_security_client.expect(r'Bluetooth MAC: (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})', timeout=30)
        .group(1)
        .decode('utf8')
    )

    gatt_security_client.expect_exact('GATT client register, status 0', timeout=30)
    gatt_security_server.expect_exact('GATT server register, status 0', timeout=30)
    gatt_security_client.expect_exact('Local privacy config successfully', timeout=30)
    gatt_security_server.expect_exact('Local privacy config successfully', timeout=30)
    gatt_security_server.expect_exact('Advertising start successfully', timeout=30)
    gatt_security_client.expect_exact('Scanning start successfully', timeout=30)
    gatt_security_client.expect_exact('Device found BE', timeout=30)
    # can not get rpa_address, so not check server address
    gatt_security_client.expect_exact(f'Connected, conn_id 0, remote ', timeout=30)
    if target == ('esp32', 'esp32'):
        gatt_security_server.expect_exact(f'Connected, conn_id 0, remote', timeout=30)
    else:
        gatt_security_server.expect_exact(f'Connected, conn_id 0, remote {gatt_security_client_addr}', timeout=30)
    gatt_security_client.expect_exact('Key exchanged, key_type ESP_LE_KEY_PID', timeout=30)
    gatt_security_client.expect_exact('Key exchanged, key_type ESP_LE_KEY_LENC', timeout=30)
    gatt_security_client.expect_exact('Key exchanged, key_type ESP_LE_KEY_PENC', timeout=30)
    gatt_security_client.expect_exact('Key exchanged, key_type ESP_LE_KEY_LID', timeout=30)

    gatt_security_server.expect_exact('Key exchanged, key_type ESP_LE_KEY_LENC', timeout=30)
    gatt_security_server.expect_exact('Key exchanged, key_type ESP_LE_KEY_PENC', timeout=30)
    gatt_security_server.expect_exact('Key exchanged, key_type ESP_LE_KEY_LID', timeout=30)
    gatt_security_server.expect_exact('Key exchanged, key_type ESP_LE_KEY_PID', timeout=30)
    if target == ('esp32', 'esp32'):
        gatt_security_server.expect_exact(f'Authentication complete, addr_type 1, addr ', timeout=30)
    else:
        gatt_security_server.expect_exact(
            f'Authentication complete, addr_type 0, addr {gatt_security_client_addr}', timeout=30
        )
    gatt_security_client.expect_exact(f'Authentication complete, addr_type 1, addr ', timeout=30)
    gatt_security_server.expect_exact('Pairing successfully', timeout=30)
    gatt_security_server.expect_exact('Bonded devices number 1', timeout=30)
    gatt_security_client.expect_exact('Pairing successfully', timeout=30)
    gatt_security_client.expect_exact('Service search complete', timeout=30)
    gatt_security_client_output = gatt_security_client.expect(pexpect.TIMEOUT, timeout=10)
    gatt_security_server_output = gatt_security_server.expect(pexpect.TIMEOUT, timeout=10)
    assert 'rst:' not in str(gatt_security_client_output) and 'boot:' not in str(gatt_security_client_output)
    assert 'rst:' not in str(gatt_security_server_output) and 'boot:' not in str(gatt_security_server_output)
    assert 'Disconnected' not in str(gatt_security_client_output)
    assert 'Disconnected' not in str(gatt_security_server_output)


# Case 4: gatt security server and gatt security client test for ESP32C2 26mhz xtal
# EXAMPLE_CI_ID=5
@pytest.mark.wifi_two_dut
@pytest.mark.xtal_26mhz
@pytest.mark.parametrize(
    'count, target, baud, app_path, config, erase_nvs',
    [
        (
            2,
            'esp32c2|esp32c2',
            '74880',
            f'{os.path.join(os.path.dirname(__file__), "gatt_security_server")}|{os.path.join(os.path.dirname(__file__), "gatt_security_client")}',
            'esp32c2_xtal26m',
            'y',
        ),
    ],
    indirect=True,
)
def test_c2_26mhz_xtal_gatt_security_func(app_path: str, dut: Tuple[IdfDut, IdfDut]) -> None:
    gatt_security_client = dut[1]
    gatt_security_server = dut[0]
    gatt_security_client_addr = (
        gatt_security_client.expect(r'Bluetooth MAC: (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})', timeout=30)
        .group(1)
        .decode('utf8')
    )

    gatt_security_client.expect_exact('GATT client register, status 0', timeout=30)
    gatt_security_server.expect_exact('GATT server register, status 0', timeout=30)
    gatt_security_client.expect_exact('Local privacy config successfully', timeout=30)
    gatt_security_server.expect_exact('Local privacy config successfully', timeout=30)
    gatt_security_server.expect_exact('Advertising start successfully', timeout=30)
    gatt_security_client.expect_exact('Scanning start successfully', timeout=30)
    gatt_security_client.expect_exact('Device found BE', timeout=30)
    # can not get rpa_address, so not check server address
    gatt_security_client.expect_exact(f'Connected, conn_id 0, remote ', timeout=30)
    gatt_security_server.expect_exact(f'Connected, conn_id 0, remote {gatt_security_client_addr}', timeout=30)
    gatt_security_client.expect_exact('Key exchanged, key_type ESP_LE_KEY_PID', timeout=30)
    gatt_security_client.expect_exact('Key exchanged, key_type ESP_LE_KEY_LENC', timeout=30)
    gatt_security_client.expect_exact('Key exchanged, key_type ESP_LE_KEY_PENC', timeout=30)
    gatt_security_client.expect_exact('Key exchanged, key_type ESP_LE_KEY_LID', timeout=30)

    gatt_security_server.expect_exact('Key exchanged, key_type ESP_LE_KEY_LENC', timeout=30)
    gatt_security_server.expect_exact('Key exchanged, key_type ESP_LE_KEY_PENC', timeout=30)
    gatt_security_server.expect_exact('Key exchanged, key_type ESP_LE_KEY_LID', timeout=30)
    gatt_security_server.expect_exact('Key exchanged, key_type ESP_LE_KEY_PID', timeout=30)
    gatt_security_server.expect_exact(
        f'Authentication complete, addr_type 0, addr {gatt_security_client_addr}', timeout=30
    )
    gatt_security_client.expect_exact(f'Authentication complete, addr_type 1, addr ', timeout=30)
    gatt_security_server.expect_exact('Pairing successfully', timeout=30)
    gatt_security_server.expect_exact('Bonded devices number 1', timeout=30)
    gatt_security_client.expect_exact('Pairing successfully', timeout=30)
    gatt_security_client.expect_exact('Service search complete', timeout=30)
    gatt_security_client_output = gatt_security_client.expect(pexpect.TIMEOUT, timeout=10)
    gatt_security_server_output = gatt_security_server.expect(pexpect.TIMEOUT, timeout=10)
    assert 'rst:' not in str(gatt_security_client_output) and 'boot:' not in str(gatt_security_client_output)
    assert 'rst:' not in str(gatt_security_server_output) and 'boot:' not in str(gatt_security_server_output)
    assert 'Disconnected' not in str(gatt_security_client_output)
    assert 'Disconnected' not in str(gatt_security_server_output)


# Case 5: ble ibeacon test
@pytest.mark.wifi_two_dut
@pytest.mark.parametrize(
    'count, app_path, config, erase_nvs',
    [
        (
            2,
            f'{os.path.join(os.path.dirname(__file__), "ble_ibeacon")}|{os.path.join(os.path.dirname(__file__), "ble_ibeacon")}',
            'sender|receiver',
            'y',
        ),
    ],
    indirect=True,
)
@idf_parametrize(
    'target', ['esp32', 'esp32c3', 'esp32c6', 'esp32c5', 'esp32h2', 'esp32s3', 'esp32c61'], indirect=['target']
)
def test_ble_ibeacon_func(app_path: str, dut: Tuple[IdfDut, IdfDut]) -> None:
    ibeacon_sender = dut[0]
    ibeacon_receiver = dut[1]

    ibeacon_sender_addr = (
        ibeacon_sender.expect(r'Bluetooth MAC: (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})', timeout=30)
        .group(1)
        .decode('utf8')
    )

    ibeacon_sender.expect_exact('Advertising start successfully', timeout=30)
    ibeacon_receiver.expect_exact('Scanning start successfully', timeout=30)
    ibeacon_receiver.expect_exact('iBeacon Found', timeout=30)
    ibeacon_receiver.expect_exact(f'IBEACON_DEMO: Device address: {ibeacon_sender_addr}', timeout=30)
    ibeacon_receiver.expect_exact('IBEACON_DEMO: Proximity UUID:', timeout=30)
    ibeacon_receiver.expect_exact('Major: 0x27b7 (10167)', timeout=30)
    ibeacon_receiver.expect_exact('Minor: 0xf206 (61958)', timeout=30)
    ibeacon_receiver.expect_exact('Measured power (RSSI at a 1m distance):', timeout=30)
    ibeacon_receiver.expect_exact('RSSI of packet: ', timeout=30)


# Case 5: ble ibeacon test for ESP32C2 26mhz xtal
@pytest.mark.wifi_two_dut
@pytest.mark.xtal_26mhz
@pytest.mark.parametrize(
    'count, target, baud, app_path, config, erase_nvs',
    [
        (
            2,
            'esp32c2|esp32c2',
            '74880',
            f'{os.path.join(os.path.dirname(__file__), "ble_ibeacon")}|{os.path.join(os.path.dirname(__file__), "ble_ibeacon")}',
            'esp32c2_xtal26m_sender|esp32c2_xtal26m_receiver',
            'y',
        ),
    ],
    indirect=True,
)
def test_c2_26mhz_ble_ibeacon_func(app_path: str, dut: Tuple[IdfDut, IdfDut]) -> None:
    ibeacon_sender = dut[0]
    ibeacon_receiver = dut[1]

    ibeacon_sender_addr = (
        ibeacon_sender.expect(r'Bluetooth MAC: (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})', timeout=30)
        .group(1)
        .decode('utf8')
    )

    ibeacon_sender.expect_exact('Advertising start successfully', timeout=30)
    ibeacon_receiver.expect_exact('Scanning start successfully', timeout=30)
    ibeacon_receiver.expect_exact('iBeacon Found', timeout=30)
    ibeacon_receiver.expect_exact(f'IBEACON_DEMO: Device address: {ibeacon_sender_addr}', timeout=30)
    ibeacon_receiver.expect_exact('IBEACON_DEMO: Proximity UUID:', timeout=30)
    ibeacon_receiver.expect_exact('Major: 0x27b7 (10167)', timeout=30)
    ibeacon_receiver.expect_exact('Minor: 0xf206 (61958)', timeout=30)
    ibeacon_receiver.expect_exact('Measured power (RSSI at a 1m distance):', timeout=30)
    ibeacon_receiver.expect_exact('RSSI of packet: ', timeout=30)


# Case 6: gatt client and gatt server config test
# EXAMPLE_CI_ID=4
@pytest.mark.wifi_two_dut
@pytest.mark.parametrize(
    'count, app_path, config, erase_nvs',
    [
        (
            2,
            f'{os.path.join(os.path.dirname(__file__), "gatt_server")}|{os.path.join(os.path.dirname(__file__), "gatt_client")}',
            'cfg_test',
            'y',
        ),
    ],
    indirect=True,
)
@idf_parametrize(
    'target', ['esp32', 'esp32c3', 'esp32c6', 'esp32c5', 'esp32h2', 'esp32s3', 'esp32c61'], indirect=['target']
)
def test_gatt_config_func(app_path: str, dut: Tuple[IdfDut, IdfDut]) -> None:
    gatt_client = dut[1]
    gatt_server = dut[0]
    gatt_client_addr = (
        gatt_client.expect(r'Bluetooth MAC: (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})', timeout=30).group(1).decode('utf8')
    )
    gatt_server_addr = (
        gatt_server.expect(r'Bluetooth MAC: (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})', timeout=30).group(1).decode('utf8')
    )
    gatt_client.expect_exact('GATT client register, status 0', timeout=30)
    gatt_server.expect_exact('GATT server register, status 0', timeout=30)
    gatt_server.expect_exact('Advertising start successfully', timeout=30)
    gatt_client.expect_exact('Scanning start successfully', timeout=30)
    gatt_client.expect_exact(f'Connected, conn_id 0, remote {gatt_server_addr}', timeout=30)
    gatt_server.expect_exact(f'Connected, conn_id 0, remote {gatt_client_addr}', timeout=30)
    gatt_client.expect_exact('Connection params update, status 0', timeout=30)
    gatt_server.expect_exact('Connection params update, status 0', timeout=30)
    gatt_client.expect_exact('Service discover complete', timeout=30)
    gatt_client.expect_exact('Service search complete', timeout=30)
    gatt_client.expect_exact('MTU exchange, status 0, MTU 500', timeout=30)
    gatt_server.expect_exact('MTU exchange, MTU 500', timeout=30)
    gatt_server.expect_exact('Notification enable', timeout=30)
    gatt_client.expect_exact('Notification received', timeout=30)
    gatt_client_output = gatt_client.expect(pexpect.TIMEOUT, timeout=10)
    gatt_server_output = gatt_server.expect(pexpect.TIMEOUT, timeout=10)
    assert 'rst:' not in str(gatt_client_output) and 'boot:' not in str(gatt_client_output)
    assert 'rst:' not in str(gatt_server_output) and 'boot:' not in str(gatt_server_output)
    assert 'Disconnected' not in str(gatt_client_output)
    assert 'Disconnected' not in str(gatt_server_output)


# Case 7: gatt client and gatt server config test for ESP32C2 26mhz xtal
# EXAMPLE_CI_ID=3
@pytest.mark.wifi_two_dut
@pytest.mark.xtal_26mhz
@pytest.mark.parametrize(
    'count, target, baud, app_path, config, erase_nvs',
    [
        (
            2,
            'esp32c2|esp32c2',
            '74880',
            f'{os.path.join(os.path.dirname(__file__), "gatt_server")}|{os.path.join(os.path.dirname(__file__), "gatt_client")}',
            'esp32c2_cfg_test',
            'y',
        ),
    ],
    indirect=True,
)
def test_c2_26mhz_xtal_gatt_config_func(app_path: str, dut: Tuple[IdfDut, IdfDut]) -> None:
    gatt_client = dut[1]
    gatt_server = dut[0]
    gatt_client_addr = (
        gatt_client.expect(r'Bluetooth MAC: (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})').group(1).decode('utf8')
    )
    gatt_server_addr = (
        gatt_server.expect(r'Bluetooth MAC: (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})').group(1).decode('utf8')
    )
    gatt_client.expect_exact('GATT client register, status 0', timeout=30)
    gatt_server.expect_exact('GATT server register, status 0', timeout=30)
    gatt_server.expect_exact('Advertising start successfully', timeout=30)
    gatt_client.expect_exact('Scanning start success', timeout=30)
    gatt_client.expect_exact(f'Connected, conn_id 0, remote {gatt_server_addr}', timeout=30)
    gatt_server.expect_exact(f'Connected, conn_id 0, remote {gatt_client_addr}', timeout=30)
    gatt_client.expect_exact('Connection params update, status 0', timeout=30)
    gatt_server.expect_exact('Connection params update, status 0', timeout=30)
    gatt_client.expect_exact('Service discover complete', timeout=30)
    gatt_client.expect_exact('Service search complete', timeout=30)
    gatt_client.expect_exact('MTU exchange, status 0, MTU 500', timeout=30)
    gatt_server.expect_exact('MTU exchange, MTU 500', timeout=30)
    gatt_server.expect_exact('Notification enable', timeout=30)
    gatt_client.expect_exact('Notification received', timeout=30)
    gatt_client_output = gatt_client.expect(pexpect.TIMEOUT, timeout=10)
    gatt_server_output = gatt_server.expect(pexpect.TIMEOUT, timeout=10)
    assert 'rst:' not in str(gatt_client_output) and 'boot:' not in str(gatt_client_output)
    assert 'rst:' not in str(gatt_server_output) and 'boot:' not in str(gatt_server_output)
    assert 'Disconnected' not in str(gatt_client_output)
    assert 'Disconnected' not in str(gatt_server_output)


# Case 8: BLE init deinit loop test
@pytest.mark.generic
@pytest.mark.parametrize(
    'config, app_path', [('init_deinit', f'{os.path.join(os.path.dirname(__file__), "gatt_client")}')], indirect=True
)
@idf_parametrize(
    'target', ['esp32c6', 'esp32h2', 'esp32c3', 'esp32s3', 'esp32c5', 'esp32c61', 'esp32'], indirect=['target']
)
def test_bluedroid_host_init_deinit(dut: Dut) -> None:
    all_hp = []
    dut.expect_exact('Bluetooth MAC:')
    for _ in range(20):
        all_hp.append(int(dut.expect(r'Free memory: (\d+) bytes').group(1).decode('utf8')))

    # the heapsize after host deinit is same
    assert len(list(set(all_hp))) == 1


# # Case 9: BLE init deinit loop test for ESP32C2 26mhz xtal
@pytest.mark.wifi_two_dut
@pytest.mark.xtal_26mhz
@pytest.mark.parametrize(
    'baud, app_path, config',
    [
        ('74880', f'{os.path.join(os.path.dirname(__file__), "gatt_client")}', 'esp32c2_init_deinit'),
    ],
    indirect=True,
)
@idf_parametrize('target', ['esp32c2'], indirect=['target'])
def test_c2_26mhz_bluedroid_host_init_deinit(dut: Dut) -> None:
    all_hp = []
    dut.expect_exact('Bluetooth MAC:')
    for _ in range(20):
        all_hp.append(int(dut.expect(r'Free memory: (\d+) bytes').group(1).decode('utf8')))

    # the heapsize after host deinit is same
    assert len(list(set(all_hp))) == 1
