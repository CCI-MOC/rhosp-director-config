'''Tests in this file apply to all hosts in the deployment (the undercloud
and all overcloud hosts).'''
import pytest

testinfra_hosts = ['ansible://overcloud', 'ansible://undercloud']


@pytest.fixture(scope='module')
def filesystems(host):
    _filesystems = []
    for fs in host.mount_point.get_mountpoints():
        if fs.filesystem not in ['ext4', 'xfs']:
            continue

        _filesystems.append(fs)

    return _filesystems


def test_restarting_containers(host):
    '''Verify that there are no restarting containers'''
    res = host.run('docker ps -f status=restarting --format={{.Names}}')
    print(res.stdout)
    assert res.exit_status == 0
    assert len(res.stdout.strip()) == 0


def test_filesystem_space(host, filesystems):
    '''Verify that filesystems have at least 10% space free'''
    for fs in filesystems:
        res = host.run(f'stat -f --format="%S %b %a" {fs.path}')
        block_size, total_blocks, free_blocks = [
            int(x) for x in res.stdout.strip().split()
        ]

        pct_blocks_free = free_blocks/total_blocks
        space_free = free_blocks * block_size
        space_total = total_blocks * block_size
        space_used = space_total - space_free

        print(f'filesystem {fs.path} '
              f'total {space_total/(1024**3):.2f} GB '
              f'free {space_free/(1024**3):.2f} GB '
              f'used {space_used/(1024**3):.2f} GB')

        assert pct_blocks_free >= 0.1
