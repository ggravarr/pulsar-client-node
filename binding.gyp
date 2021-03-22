#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

{
  "targets": [
    {
      "target_name": "<(module_name)",
      "cflags!": ["-fno-exceptions"],
      "cflags_cc!": ["-fno-exceptions"],
      "include_dirs": ["<!@(node -p \"require('node-addon-api').include\")"],
      "dependencies": ["<!@(node -p \"require('node-addon-api').gyp\")"],
      "defines": ["NAPI_DISABLE_CPP_EXCEPTIONS"],
      "sources": [
        "src/addon.cc",
        "src/Message.cc",
        "src/MessageId.cc",
        "src/Authentication.cc",
        "src/Client.cc",
        "src/Producer.cc",
        "src/ProducerConfig.cc",
        "src/Consumer.cc",
        "src/ConsumerConfig.cc",
        "src/Reader.cc",
        "src/ReaderConfig.cc",
      ],
      "conditions":[
      	["OS=='linux'", {
      	  "libraries": [ "/usr/lib/libpulsarwithdeps.a" ]
        }],
      	["OS=='mac'", {
          "actions": [{
            "action_name": "build_libpulsar_mac",
            "inputs": [
              "<(module_root_dir)/build-support/build-mac.sh"
            ],
            "outputs": [
              "<(module_root_dir)/build-support/libpulsarwithdeps.a"
            ],
            "action": ["bash", "build-support/build-mac.sh"]
          }],
      	  "libraries": [
            "<(module_root_dir)/build-support/libpulsarwithdeps.a",
            "<!(brew --prefix)/opt/curl/lib/libcurl.a",
            "<!(brew --prefix)/opt/openssl/lib/libcrypto.a",
            "<!(brew --prefix)/opt/openssl/lib/libssl.a",
            "<!(brew --prefix)/opt/libssh2/lib/libssh2.a"
          ],
          "xcode_settings": {
            "MACOSX_DEPLOYMENT_TARGET": "10.15",
            "OTHER_LDFLAGS": [
              "-L<!(brew --prefix)/opt/openssl/lib",
              "-L<!(brew --prefix)/opt/libssh2/lib",
              "-framework Security",
              "-framework Kerberos",
              "-framework GSS"
            ],
            "OTHER_CPLUSPLUSFLAGS": [
              "-I<!(brew --prefix)/opt/openssl/include",
              "-I<!(brew --prefix)/opt/libssh2/include",
              "-std=c++11"
             ]
          }
      	}]
      ],
    },
    {
      "target_name": "action_after_build",
      "type": "none",
      "dependencies": ["<(module_name)"],
      "copies": [
        {
          "files": ["<(PRODUCT_DIR)/<(module_name).node"],
          "destination": "<(module_path)"
        }
      ]
    }
  ]
}
