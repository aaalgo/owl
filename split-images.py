#!/usr/bin/env python

import argparse
import sys
import cv2
import numpy as np

# reads a list of paths from stdin
# split the images and write to an output directory

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('--out', required=True, help='output directory')
    parser.add_argument('--step', default=400, type=int, help='')
    parser.add_argument('--ext', default='.jpg', help='')

    args = parser.parse_args() 

    S = args.step

    ci = 0
    for l in sys.stdin:
        l = l.strip()
        image = cv2.imread(l)
        H, W = image.shape[:2]
        row = 0
        for h in range(0, H, S):
            if h + S > H:
                h = H - S
            col = 0
            for w in range(0, W, S):
                if w + S > W:
                    w = W - S
                patch = image[h:(h+S), w:(w+S)]
                cv2.imwrite('%s/%d-%d-%d%s' % (args.out, ci, row, col, args.ext), patch)
                col += 1
                pass
            row += 1
            pass
        ci+=1
        pass
    pass





