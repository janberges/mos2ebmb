#!/bin/bash

tar -czvf fig2e.tar.gz --exclude='.git*' --exclude='archive.sh' --transform='s,^,fig2e/,' `git ls-files`
