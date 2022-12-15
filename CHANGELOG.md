# Changelog

<!--next-version-placeholder-->

## v0.19.3 (2022-12-15)
### Fix
* Reject impossible temp values take 2 ([#50](https://github.com/Bluetooth-Devices/govee-ble/issues/50)) ([`c0a54eb`](https://github.com/Bluetooth-Devices/govee-ble/commit/c0a54eb3e00afe20bacbb930ea8ce251d760d8bc))

## v0.19.2 (2022-12-15)
### Fix
* Reject impossible temp values ([#47](https://github.com/Bluetooth-Devices/govee-ble/issues/47)) ([`bb8b6e0`](https://github.com/Bluetooth-Devices/govee-ble/commit/bb8b6e00b8c0a2a8779806e6b25330ef50cb41f8))

## v0.19.1 (2022-09-30)
### Fix
* Handle another H5181 ([#45](https://github.com/Bluetooth-Devices/govee-ble/issues/45)) ([`af2da30`](https://github.com/Bluetooth-Devices/govee-ble/commit/af2da30574db19674ec5e76bfaa5c84adcbbe9f0))

## v0.19.0 (2022-09-24)
### Feature
* Add support for yet another H5183 variant ([#44](https://github.com/Bluetooth-Devices/govee-ble/issues/44)) ([`d699552`](https://github.com/Bluetooth-Devices/govee-ble/commit/d699552bef2c3be13b34899f34e355a54914ffdb))

## v0.18.0 (2022-09-24)
### Feature
* Add support for another H5181 variant ([#43](https://github.com/Bluetooth-Devices/govee-ble/issues/43)) ([`7738d25`](https://github.com/Bluetooth-Devices/govee-ble/commit/7738d25fe6737a2c41d4d1f7af6e3fa41861ba0e))

## v0.17.3 (2022-09-13)
### Fix
* Publish ([#41](https://github.com/Bluetooth-Devices/govee-ble/issues/41)) ([`40ce706`](https://github.com/Bluetooth-Devices/govee-ble/commit/40ce70653f9cd52eb584253f6893d0f20677d2c7))

## v0.17.2 (2022-09-05)
### Fix
* Names are now human readable ([#39](https://github.com/Bluetooth-Devices/govee-ble/issues/39)) ([`fefc6b4`](https://github.com/Bluetooth-Devices/govee-ble/commit/fefc6b405e62a063234d12c8d812f9581b24369c))

## v0.17.1 (2022-08-31)
### Fix
* Model H5181 var fixes ([#38](https://github.com/Bluetooth-Devices/govee-ble/issues/38)) ([`42012bc`](https://github.com/Bluetooth-Devices/govee-ble/commit/42012bc8be9028c62054a7b143ea990ffeb67deb))

## v0.17.0 (2022-08-30)
### Feature
* Add support for additional H5185 firmware ([#37](https://github.com/Bluetooth-Devices/govee-ble/issues/37)) ([`0a5dfa5`](https://github.com/Bluetooth-Devices/govee-ble/commit/0a5dfa5e4e95d79f3f9a5e076355963ba75d34be))

## v0.16.1 (2022-08-25)
### Fix
* Use bluetooth-data-tools short_address ([#36](https://github.com/Bluetooth-Devices/govee-ble/issues/36)) ([`e137d93`](https://github.com/Bluetooth-Devices/govee-ble/commit/e137d930d7605a41f7112fd342cfc4bd269dc7da))

## v0.16.0 (2022-08-16)
### Feature
* Add support for H5071 ([#34](https://github.com/Bluetooth-Devices/govee-ble/issues/34)) ([`cf7e809`](https://github.com/Bluetooth-Devices/govee-ble/commit/cf7e8095c3f15a5d2ccde2cd14cf294edb4ba379))

## v0.15.0 (2022-08-16)
### Feature
* Implement rounding ([#33](https://github.com/Bluetooth-Devices/govee-ble/issues/33)) ([`eeed1aa`](https://github.com/Bluetooth-Devices/govee-ble/commit/eeed1aa231be0df9f3193511124ca2dfeeeaee51))

## v0.14.1 (2022-08-11)
### Fix
* Older 5181 firmwares ([#31](https://github.com/Bluetooth-Devices/govee-ble/issues/31)) ([`61eac60`](https://github.com/Bluetooth-Devices/govee-ble/commit/61eac6038177b58c07a80882d3cebe9debc25430))

## v0.14.0 (2022-08-08)
### Feature
* Add support for the h5052 ([#30](https://github.com/Bluetooth-Devices/govee-ble/issues/30)) ([`625594c`](https://github.com/Bluetooth-Devices/govee-ble/commit/625594c16ad67801cf2a57fa2534900e6ef28310))

## v0.13.0 (2022-08-08)
### Feature
* Add support for the 5184 devices ([#29](https://github.com/Bluetooth-Devices/govee-ble/issues/29)) ([`d9d6d6a`](https://github.com/Bluetooth-Devices/govee-ble/commit/d9d6d6a84e7b7647c829be8471915e15fa61ca0d))

## v0.12.7 (2022-08-07)
### Fix
* Add 818 to the manufacturer_ids for the gvh5185 ([#28](https://github.com/Bluetooth-Devices/govee-ble/issues/28)) ([`f3cfb61`](https://github.com/Bluetooth-Devices/govee-ble/commit/f3cfb61c2d562b801570956901f669c27b0d77fb))

## v0.12.6 (2022-08-02)
### Fix
* The GVH5074 is little endian ([#27](https://github.com/Bluetooth-Devices/govee-ble/issues/27)) ([`28e626c`](https://github.com/Bluetooth-Devices/govee-ble/commit/28e626c2527c395c507fbe00e7f18a184a3484f0))

## v0.12.5 (2022-07-30)
### Fix
* H5179 is little endian and not big endian like the rest ([#26](https://github.com/Bluetooth-Devices/govee-ble/issues/26)) ([`24a0e92`](https://github.com/Bluetooth-Devices/govee-ble/commit/24a0e922f32ef476d51d0b13e90a737dfdc83676))

## v0.12.4 (2022-07-29)
### Fix
* Parser for h5182 had the wrong mfgr_id ([#25](https://github.com/Bluetooth-Devices/govee-ble/issues/25)) ([`57abb96`](https://github.com/Bluetooth-Devices/govee-ble/commit/57abb962b32994fe4ec8cb938ad89947838b8294))

## v0.12.3 (2022-07-22)
### Fix
* Names for bbq devices ([#24](https://github.com/Bluetooth-Devices/govee-ble/issues/24)) ([`4407ed4`](https://github.com/Bluetooth-Devices/govee-ble/commit/4407ed431f4280ca77b7a31cd4fa930f878aee77))

## v0.12.2 (2022-07-22)
### Fix
* Fixs for bbq sensors ([#23](https://github.com/Bluetooth-Devices/govee-ble/issues/23)) ([`132d04d`](https://github.com/Bluetooth-Devices/govee-ble/commit/132d04d91fc9161ff1a67a34c9b00c46afb2f708))

## v0.12.1 (2022-07-21)
### Fix
* Bump sensor-state-data to fix typing ([#22](https://github.com/Bluetooth-Devices/govee-ble/issues/22)) ([`d5cdfc5`](https://github.com/Bluetooth-Devices/govee-ble/commit/d5cdfc506abeb4c81bbb0c2d0c7515f7c81266c5))

## v0.12.0 (2022-07-21)
### Feature
* Refactor for sensor-state-data 2 ([#21](https://github.com/Bluetooth-Devices/govee-ble/issues/21)) ([`b7fb4dc`](https://github.com/Bluetooth-Devices/govee-ble/commit/b7fb4dcef279e1eeb4b53e47e8f684c3a785e3c2))

## v0.11.0 (2022-07-20)
### Feature
* Export SensorDescription and SensorValue ([#20](https://github.com/Bluetooth-Devices/govee-ble/issues/20)) ([`b61e938`](https://github.com/Bluetooth-Devices/govee-ble/commit/b61e938ce974bf892b2060bc95d6ee808191d1bf))

## v0.10.2 (2022-07-20)
### Fix
* Bump deps ([#19](https://github.com/Bluetooth-Devices/govee-ble/issues/19)) ([`5fc9ece`](https://github.com/Bluetooth-Devices/govee-ble/commit/5fc9ece3d7502bfab84f9f287912f6375549cf49))

## v0.10.1 (2022-07-19)
### Fix
* Bump libs ([#18](https://github.com/Bluetooth-Devices/govee-ble/issues/18)) ([`e818e7c`](https://github.com/Bluetooth-Devices/govee-ble/commit/e818e7c4dc797a571e1d78426f62b940ec60c585))

## v0.10.0 (2022-07-19)
### Feature
* Export all needed objects ([#17](https://github.com/Bluetooth-Devices/govee-ble/issues/17)) ([`3c5ca7b`](https://github.com/Bluetooth-Devices/govee-ble/commit/3c5ca7b42d20c36bcca650ba15b4b32280751a88))

## v0.9.1 (2022-07-19)
### Fix
* Add missing device classes to bbq probes ([#16](https://github.com/Bluetooth-Devices/govee-ble/issues/16)) ([`f2cafd7`](https://github.com/Bluetooth-Devices/govee-ble/commit/f2cafd71dba9894cb7dc9ab6706bd23b77c61366))

## v0.9.0 (2022-07-19)
### Feature
* Set manu for secondary sensor ([#15](https://github.com/Bluetooth-Devices/govee-ble/issues/15)) ([`ec54d57`](https://github.com/Bluetooth-Devices/govee-ble/commit/ec54d57f25bdff968d9430421b64a751f1b2ce13))

## v0.8.0 (2022-07-19)
### Feature
* Add set_device_manufacturer ([#14](https://github.com/Bluetooth-Devices/govee-ble/issues/14)) ([`f0203b7`](https://github.com/Bluetooth-Devices/govee-ble/commit/f0203b7c50753127f298e7d7c6977580dccb8cd4))

## v0.7.0 (2022-07-19)
### Feature
* Add support for B5178 local name variation ([#13](https://github.com/Bluetooth-Devices/govee-ble/issues/13)) ([`324b3cd`](https://github.com/Bluetooth-Devices/govee-ble/commit/324b3cd99c833496af7427333e591f23d249ec70))

## v0.6.0 (2022-07-19)
### Feature
* Do not drop mac from title ([#12](https://github.com/Bluetooth-Devices/govee-ble/issues/12)) ([`cd187ed`](https://github.com/Bluetooth-Devices/govee-ble/commit/cd187ed19b0acf5b7b0c3a91dbc0e13fb321cce5))

## v0.5.0 (2022-07-19)
### Feature
* Set title for outdoor sensors ([#11](https://github.com/Bluetooth-Devices/govee-ble/issues/11)) ([`1031c78`](https://github.com/Bluetooth-Devices/govee-ble/commit/1031c782865e9b6ec74e38df5f3b4a5345d871ce))

## v0.4.1 (2022-07-19)
### Fix
* Fix device_id for remote sensors ([#10](https://github.com/Bluetooth-Devices/govee-ble/issues/10)) ([`198caf2`](https://github.com/Bluetooth-Devices/govee-ble/commit/198caf26a535f070921ee3e24cc66070d64282d2))

## v0.4.0 (2022-07-19)
### Feature
* Improve support for remote sensors ([#9](https://github.com/Bluetooth-Devices/govee-ble/issues/9)) ([`bf6eca1`](https://github.com/Bluetooth-Devices/govee-ble/commit/bf6eca1d1f64770fd010475afaeeb642c5e175ff))

## v0.3.0 (2022-07-19)
### Feature
* Change model ([#8](https://github.com/Bluetooth-Devices/govee-ble/issues/8)) ([`9456bb3`](https://github.com/Bluetooth-Devices/govee-ble/commit/9456bb3ec459e9f2e7d7be4e1bfd670e5cb4fed6))

## v0.2.1 (2022-07-19)
### Fix
* Update sensor-state-data ([#7](https://github.com/Bluetooth-Devices/govee-ble/issues/7)) ([`02b04a9`](https://github.com/Bluetooth-Devices/govee-ble/commit/02b04a91d47337dbdd925cc2c7e037500cd934f2))

## v0.2.0 (2022-07-19)
### Feature
* Switch to using bluetooth-sensor-state-data ([#6](https://github.com/Bluetooth-Devices/govee-ble/issues/6)) ([`8ad3ec5`](https://github.com/Bluetooth-Devices/govee-ble/commit/8ad3ec5f8e7117cf1847be79641b1f706eb9478f))

## v0.1.1 (2022-07-18)
### Fix
* Fix links ([#5](https://github.com/Bluetooth-Devices/govee-ble/issues/5)) ([`455f2d2`](https://github.com/Bluetooth-Devices/govee-ble/commit/455f2d202e80c03bb0e15d1f0385316e3d9dfded))

## v0.1.0 (2022-07-18)
### Feature
* Init repo ([#2](https://github.com/Bluetooth-Devices/govee-ble/issues/2)) ([`58fe30c`](https://github.com/Bluetooth-Devices/govee-ble/commit/58fe30ca51b74e3c822bb03e3876eced657915a8))

### Fix
* Fix publish process ([#4](https://github.com/Bluetooth-Devices/govee-ble/issues/4)) ([`9c3f892`](https://github.com/Bluetooth-Devices/govee-ble/commit/9c3f89271d1226f05dbe6ec972096c2e822bd2bb))

## v0.0.2 (2022-07-18)
### Fix
* Bump python min to 3.9 ([`5913902`](https://github.com/Bluetooth-Devices/govee-ble/commit/5913902dd854a5e3fc86e290e76fcb8eef9d1804))
