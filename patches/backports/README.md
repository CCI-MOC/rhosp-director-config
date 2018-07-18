We're carrying some patches, many of which are still under review
upstream.  These directories contain backports of those patches
against the RHOSP 13 packages.

  - https://review.openstack.org/#/q/I200011e2e0ffd01a2aa26df8a03f03151eb64150
  - https://review.openstack.org/#/q/I9ff976854b93cdf9ca3175d1fd39c2b268b9f7fa
  - https://review.openstack.org/#/q/Ib79fbd47169388bfb044a8183725a3d1de5bc480
  - https://review.openstack.org/#/q/Id2ef3558a359883bf3182f50d6a082b1789a900a
  - https://review.openstack.org/#/q/I58e364a3a6c0ebc7bc57ff5821ccdb882324ff81
  - https://review.openstack.org/#/q/I14b540e6564c5b7c5d54b4f1fd5368b000744135
  - https://review.openstack.org/#/q/Ifd8b7dea83a4566b69f76898952f908395c590a4
  - https://review.openstack.org/#/q/I3e06ca5fde65f3e2c3c084f96209d1b38d5f8b86
  - https://review.openstack.org/#/q/Iff0abdfd7605d839e8ab145078de523864db4660
  - https://review.openstack.org/#/q/I89cff59947dda3f51482486c41a3d67c4aa36a3e

To generate the above list, run the following:

    grep -ri change-id */*patch | awk '{printf "  - https://review.openstack.org/#/q/%s\n", $NF}'
