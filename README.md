# Git benchmark
A toy project to benchmark git.

## Cloning
How fast can we clone a large git repo so that it can be analyzed.

Some resources on cloning repositories:
- https://github.blog/open-source/git/get-up-to-speed-with-partial-clone-and-shallow-clone/


### Full clone
This clone all commits, trees and blobs from a git repository.
Full cloning rails takes 8.5 seconds.
```
➜  repos git:(master) ✗ time git clone git@github.com:rails/rails.git rails_full_clone
Cloning into 'rails_full_clone'...
remote: Enumerating objects: 885160, done.
remote: Counting objects: 100% (2/2), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 885160 (delta 0), reused 0 (delta 0), pack-reused 885158 (from 1)
Receiving objects: 100% (885160/885160), 276.41 MiB | 63.59 MiB/s, done.
Resolving deltas: 100% (661265/661265), done.

git clone git@github.com:rails/rails.git rails_full_clone  16.48s user 8.12s system 279% cpu 8.812 total
```


### Partial clone
This clones all commits and trees, but not the blobs that are not needed. Can reduce clone size by 10x on large repositories.
Partially cloning rails takes 5.2 seconds.
```
➜  repos git:(master) ✗ time git clone --filter=blob:none git@github.com:rails/rails.git rails_partial_clone
Cloning into 'rails_partial_clone'...
remote: Enumerating objects: 670905, done.
remote: Counting objects: 100% (1/1), done.
remote: Total 670905 (delta 0), reused 0 (delta 0), pack-reused 670904 (from 1)
Receiving objects: 100% (670905/670905), 98.15 MiB | 71.18 MiB/s, done.
Resolving deltas: 100% (471888/471888), done.
remote: Enumerating objects: 4403, done.
remote: Counting objects: 100% (2465/2465), done.
remote: Compressing objects: 100% (2342/2342), done.
remote: Total 4403 (delta 261), reused 123 (delta 123), pack-reused 1938 (from 1)
Receiving objects: 100% (4403/4403), 8.70 MiB | 15.52 MiB/s, done.
Resolving deltas: 100% (381/381), done.
Updating files: 100% (4719/4719), done.

git clone --filter=blob:none git@github.com:rails/rails.git   3.69s user 1.91s system 106% cpu 5.251 total
```

### Shallow clone
This clones the trees and blobs only for the tip commit. Any access to information of older commits will require a network fetch.
This is useful when you really only need a snapshot of the codebase as it is in its latest version. It sucks if you need to read its history.
