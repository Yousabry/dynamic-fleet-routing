import matplotlib.pyplot as plt

ff_bus_utility = {None: 57986, 281: 132, 586: 132, 324: 131, 731: 131, 27: 130, 672: 129, 524: 128, 290: 126, 788: 126, 240: 126, 458: 125, 85: 124, 667: 124, 817: 124, 660: 124, 12: 123, 774: 122, 341: 122, 165: 122, 214: 121, 135: 121, 427: 121, 628: 121, 822: 121, 805: 121, 147: 121, 494: 120, 419: 120, 259: 120, 840: 120, 614: 119, 519: 119, 436: 119, 835: 119, 762: 119, 888: 119, 464: 119, 456: 119, 291: 119, 292: 118, 876: 118, 434: 118, 130: 118, 834: 118, 395: 118, 84: 117, 54: 117, 404: 117, 79: 117, 644: 117, 298: 117, 57: 117, 264: 117, 412: 116, 52: 116, 171: 116, 114: 116, 245: 116, 819: 116, 755: 116, 758: 116, 63: 116, 314: 116, 808: 116, 406: 116, 581: 116, 424: 116, 152: 116, 455: 116, 630: 115, 793: 115, 811: 115, 863: 115, 210: 115, 416: 115, 739: 115, 474: 115, 620: 115, 490: 115, 505: 115, 378: 114, 169: 114, 695: 114, 49: 114, 414: 114, 673: 114, 710: 114, 679: 114, 504: 114, 149: 114, 70: 114, 351: 114, 463: 114, 106: 114, 132: 113, 638: 113, 156: 113, 779: 113, 78: 113, 752: 113, 192: 113, 652: 113, 280: 113, 180: 113, 576: 113, 235: 113, 36: 113, 175: 113, 101: 113, 185: 113, 498: 113, 777: 113, 73: 112, 1: 112, 442: 112, 475: 112, 542: 112, 857: 112, 39: 112, 801: 112, 166: 112, 352: 112, 331: 112, 635: 112, 678: 112, 481: 112, 340: 112, 208: 112, 388: 112, 426: 112, 839: 112, 709: 111, 601: 111, 326: 111, 213: 111, 159: 111, 613: 111, 178: 111, 177: 111, 448: 111, 532: 111, 610: 111, 594: 111, 574: 111, 615: 111, 737: 111, 794: 111, 244: 111, 479: 111, 14: 111, 503: 111, 21: 111, 407: 111, 370: 111, 785: 111, 38: 111, 170: 110, 790: 110, 8: 110, 648: 110, 90: 110, 107: 110, 429: 110, 803: 110, 398: 110, 195: 110, 836: 110, 680: 110, 621: 110, 826: 110, 380: 110, 399: 110, 795: 110, 3: 110, 650: 110, 275: 110, 425: 110, 286: 110, 664: 110, 276: 110, 548: 109, 675: 109, 179: 109, 832: 109, 10: 109, 683: 109, 330: 109, 322: 109, 255: 109, 895: 109, 452: 109, 789: 109, 626: 109, 697: 109, 9: 109, 587: 109, 691: 109, 411: 109, 218: 109, 30: 109, 347: 109, 154: 109, 167: 109, 501: 109, 105: 109, 41: 109, 898: 109, 657: 109, 619: 109, 608: 109, 94: 109, 144: 109, 222: 109, 488: 108, 892: 108, 67: 108, 68: 108, 338: 108, 890: 108, 549: 108, 606: 108, 534: 108, 699: 108, 773: 108, 521: 108, 440: 108, 491: 108, 196: 108, 859: 108, 763: 108, 65: 108, 690: 108, 531: 108, 866: 108, 432: 108, 743: 108, 272: 108, 120: 108, 190: 108, 730: 108, 383: 108, 435: 108, 643: 108, 847: 107, 599: 107, 513: 107, 655: 107, 224: 107, 550: 107, 131: 107, 891: 107, 278: 107, 689: 107, 18: 107, 674: 107, 528: 107, 647: 107, 99: 107, 804: 107, 271: 107, 293: 107, 142: 107, 19: 107, 81: 107, 367: 107, 379: 107, 799: 107, 129: 107, 671: 107, 460: 107, 237: 107, 787: 107, 708: 107, 560: 107, 712: 107, 706: 107, 659: 107, 492: 107, 303: 107, 401: 107, 571: 107, 751: 107, 128: 107, 851: 107, 882: 106, 681: 106, 437: 106, 284: 106, 139: 106, 512: 106, 104: 106, 223: 106, 735: 106, 155: 106, 495: 106, 82: 106, 716: 106, 342: 106, 509: 106, 302: 106, 703: 106, 651: 106, 600: 106, 394: 106, 470: 106, 539: 106, 61: 106, 740: 106, 605: 106, 4: 106, 810: 106, 234: 106, 843: 106, 87: 106, 761: 106, 301: 106, 666: 106, 332: 106, 23: 106, 525: 106, 582: 106, 141: 106, 569: 106, 623: 106, 637: 105, 661: 105, 883: 105, 198: 105, 665: 105, 485: 105, 596: 105, 482: 105, 300: 105, 206: 105, 389: 105, 362: 105, 536: 105, 308: 105, 578: 105, 197: 105, 53: 105, 327: 105, 860: 105, 854: 105, 315: 105, 447: 105, 687: 105, 780: 105, 802: 105, 562: 105, 625: 105, 618: 105, 700: 105, 2: 105, 508: 105, 433: 105, 465: 105, 641: 105, 413: 105, 334: 105, 226: 104, 358: 104, 556: 104, 22: 104, 346: 104, 265: 104, 768: 104, 526: 104, 5: 104, 842: 104, 306: 104, 734: 104, 896: 104, 133: 104, 381: 104, 44: 104, 317: 104, 371: 104, 544: 104, 253: 104, 140: 104, 807: 104, 588: 104, 307: 104, 677: 104, 879: 104, 591: 104, 572: 104, 204: 104, 759: 104, 181: 104, 558: 103, 533: 103, 221: 103, 108: 103, 219: 103, 34: 103, 772: 103, 110: 103, 814: 103, 339: 103, 199: 103, 203: 103, 354: 103, 736: 103, 415: 103, 776: 103, 565: 103, 884: 103, 784: 103, 861: 103, 707: 103, 212: 103, 725: 103, 231: 103, 738: 103, 893: 103, 48: 103, 506: 103, 386: 103, 609: 103, 476: 103, 500: 103, 844: 103, 473: 103, 344: 103, 283: 103, 150: 103, 831: 103, 402: 102, 345: 102, 420: 102, 848: 102, 288: 102, 103: 102, 577: 102, 64: 102, 663: 102, 449: 102, 497: 102, 46: 102, 241: 102, 585: 102, 37: 102, 849: 102, 98: 102, 726: 102, 559: 102, 350: 102, 77: 102, 543: 102, 616: 102, 873: 102, 568: 102, 547: 102, 824: 102, 124: 102, 418: 102, 579: 102, 653: 102, 717: 102, 393: 101, 806: 101, 446: 101, 649: 101, 698: 101, 343: 101, 870: 101, 15: 101, 624: 101, 24: 101, 792: 101, 157: 101, 858: 101, 118: 101, 59: 101, 724: 101, 372: 101, 200: 101, 443: 101, 775: 101, 669: 101, 718: 101, 186: 101, 127: 101, 396: 101, 845: 101, 183: 101, 656: 101, 111: 101, 400: 101, 262: 101, 363: 101, 732: 101, 359: 101, 194: 101, 189: 101, 454: 101, 62: 101, 172: 101, 749: 101, 25: 101, 748: 100, 704: 100, 377: 100, 349: 100, 554: 100, 385: 100, 639: 100, 258: 100, 887: 100, 50: 100, 376: 100, 786: 100, 540: 100, 428: 100, 209: 100, 163: 100, 312: 100, 268: 100, 207: 100, 316: 100, 640: 100, 397: 100, 765: 100, 122: 100, 692: 100, 366: 100, 522: 100, 319: 100, 575: 100, 631: 100, 45: 100, 274: 100, 125: 100, 520: 100, 880: 100, 260: 100, 277: 100, 95: 100, 239: 100, 364: 100, 589: 100, 627: 100, 598: 100, 714: 100, 477: 100, 313: 100, 750: 99, 450: 99, 116: 99, 13: 99, 451: 99, 287: 99, 109: 99, 705: 99, 299: 99, 188: 99, 723: 99, 821: 99, 583: 99, 684: 99, 249: 99, 676: 99, 864: 99, 136: 99, 769: 99, 693: 99, 471: 99, 289: 99, 662: 99, 827: 99, 713: 99, 527: 99, 56: 99, 457: 99, 86: 99, 76: 99, 42: 99, 261: 99, 553: 99, 444: 99, 205: 99, 335: 99, 438: 98, 375: 98, 227: 98, 353: 98, 134: 98, 592: 98, 555: 98, 409: 98, 43: 98, 422: 98, 871: 98, 184: 98, 798: 98, 541: 98, 162: 98, 461: 98, 856: 98, 145: 98, 368: 98, 557: 98, 250: 98, 853: 98, 818: 98, 91: 98, 830: 98, 869: 98, 607: 98, 266: 98, 517: 98, 770: 98, 310: 98, 257: 98, 74: 98, 355: 97, 7: 97, 246: 97, 191: 97, 820: 97, 217: 97, 894: 97, 29: 97, 766: 97, 828: 97, 551: 97, 727: 97, 530: 97, 682: 97, 232: 97, 511: 97, 294: 97, 282: 97, 410: 97, 311: 97, 468: 97, 158: 97, 33: 97, 123: 97, 88: 97, 269: 97, 867: 97, 515: 97, 877: 97, 720: 97, 423: 97, 325: 97, 256: 97, 462: 97, 702: 97, 336: 97, 573: 96, 862: 96, 537: 96, 47: 96, 841: 96, 369: 96, 881: 96, 309: 96, 320: 96, 670: 96, 868: 96, 825: 96, 26: 96, 417: 96, 441: 96, 392: 96, 612: 96, 115: 96, 545: 96, 193: 96, 686: 96, 467: 96, 92: 96, 855: 96, 760: 96, 373: 96, 850: 96, 391: 96, 552: 96, 248: 96, 764: 96, 815: 96, 137: 96, 230: 95, 72: 95, 634: 95, 126: 95, 0: 95, 489: 95, 17: 95, 102: 95, 58: 95, 646: 95, 711: 95, 267: 95, 174: 95, 645: 95, 356: 95, 636: 95, 100: 95, 622: 95, 328: 95, 563: 95, 182: 95, 93: 95, 654: 95, 889: 95, 6: 95, 374: 95, 469: 95, 778: 95, 173: 95, 523: 95, 228: 95, 745: 95, 480: 95, 499: 95, 113: 95, 321: 94, 430: 94, 566: 94, 809: 94, 812: 94, 323: 94, 117: 94, 696: 94, 595: 94, 220: 94, 694: 94, 297: 94, 733: 94, 31: 94, 746: 94, 564: 94, 783: 94, 496: 94, 28: 94, 593: 94, 658: 94, 507: 94, 403: 94, 816: 94, 757: 94, 148: 94, 833: 94, 813: 94, 83: 94, 40: 93, 872: 93, 254: 93, 119: 93, 243: 93, 431: 93, 472: 93, 143: 93, 285: 93, 138: 93, 160: 93, 796: 93, 603: 93, 538: 93, 318: 93, 668: 93, 329: 93, 459: 93, 721: 93, 838: 93, 529: 93, 382: 93, 337: 93, 146: 93, 837: 93, 408: 93, 439: 93, 16: 93, 518: 93, 55: 93, 535: 93, 597: 93, 242: 92, 229: 92, 493: 92, 252: 92, 617: 92, 483: 92, 60: 92, 782: 92, 791: 92, 201: 92, 688: 92, 466: 92, 561: 92, 629: 92, 715: 92, 874: 91, 20: 91, 296: 91, 365: 91, 580: 91, 11: 91, 886: 91, 405: 91, 35: 91, 846: 91, 333: 91, 685: 91, 233: 91, 304: 91, 97: 91, 225: 91, 729: 91, 878: 91, 279: 91, 121: 91, 514: 91, 161: 90, 202: 90, 69: 90, 71: 90, 781: 90, 216: 90, 32: 90, 251: 90, 51: 90, 604: 90, 744: 90, 487: 90, 484: 90, 747: 90, 899: 90, 478: 90, 445: 90, 722: 90, 719: 90, 236: 90, 305: 89, 153: 89, 829: 89, 602: 89, 756: 89, 176: 89, 66: 89, 642: 89, 247: 89, 348: 89, 168: 89, 361: 89, 421: 89, 384: 89, 800: 88, 633: 88, 546: 88, 89: 88, 753: 88, 885: 88, 742: 88, 486: 88, 852: 88, 823: 88, 238: 88, 701: 88, 112: 87, 797: 87, 570: 87, 80: 87, 502: 87, 611: 87, 875: 86, 567: 86, 632: 86, 215: 86, 516: 86, 584: 86, 273: 86, 151: 85, 360: 85, 357: 85, 453: 85, 387: 85, 741: 84, 390: 84, 754: 84, 295: 84, 270: 84, 164: 84, 263: 83, 211: 82, 96: 82, 187: 81, 771: 81, 897: 80, 590: 80, 728: 79, 767: 79, 75: 79, 510: 77, 865: 76}
gc_bus_utility = {None: 67586, 868: 119, 607: 112, 627: 112, 306: 111, 124: 111, 727: 110, 259: 110, 294: 110, 303: 110, 354: 109, 232: 109, 599: 108, 392: 108, 591: 108, 184: 108, 556: 107, 258: 107, 821: 107, 783: 107, 301: 107, 125: 107, 523: 107, 103: 106, 683: 106, 174: 106, 293: 106, 453: 106, 366: 106, 468: 106, 476: 106, 883: 105, 489: 105, 271: 105, 419: 105, 84: 105, 41: 105, 706: 105, 465: 105, 425: 105, 537: 104, 663: 104, 438: 104, 224: 104, 35: 104, 710: 104, 290: 104, 575: 104, 221: 103, 595: 103, 130: 103, 789: 103, 555: 103, 375: 103, 188: 103, 750: 103, 242: 103, 467: 103, 810: 103, 66: 103, 649: 102, 741: 102, 894: 102, 26: 102, 377: 102, 40: 102, 776: 102, 17: 102, 167: 102, 342: 102, 44: 102, 521: 102, 610: 102, 443: 102, 60: 102, 869: 102, 173: 102, 721: 102, 570: 102, 761: 102, 455: 102, 809: 101, 255: 101, 151: 101, 73: 101, 825: 101, 356: 101, 252: 101, 49: 101, 494: 101, 692: 101, 680: 101, 459: 101, 864: 101, 898: 101, 418: 101, 568: 101, 805: 101, 201: 101, 890: 100, 526: 100, 67: 100, 639: 100, 754: 100, 472: 100, 602: 100, 734: 100, 114: 100, 29: 100, 628: 100, 696: 100, 662: 100, 767: 100, 669: 100, 155: 100, 565: 100, 522: 100, 604: 100, 474: 100, 481: 100, 705: 100, 479: 100, 424: 100, 382: 100, 658: 100, 36: 100, 91: 100, 55: 100, 25: 100, 22: 99, 428: 99, 847: 99, 475: 99, 774: 99, 309: 99, 346: 99, 211: 99, 39: 99, 724: 99, 213: 99, 651: 99, 576: 99, 193: 99, 177: 99, 471: 99, 447: 99, 504: 99, 687: 99, 856: 99, 180: 99, 158: 99, 743: 99, 383: 99, 818: 99, 629: 99, 738: 99, 336: 99, 722: 99, 137: 99, 223: 98, 554: 98, 110: 98, 191: 98, 578: 98, 10: 98, 792: 98, 784: 98, 842: 98, 797: 98, 665: 98, 195: 98, 209: 98, 210: 98, 716: 98, 43: 98, 381: 98, 855: 98, 814: 98, 368: 98, 53: 98, 744: 98, 729: 98, 733: 98, 183: 98, 889: 98, 853: 98, 616: 98, 823: 98, 332: 98, 94: 98, 515: 98, 531: 98, 581: 98, 113: 98, 454: 98, 172: 98, 370: 98, 214: 97, 108: 97, 596: 97, 178: 97, 157: 97, 458: 97, 888: 97, 345: 97, 440: 97, 684: 97, 811: 97, 411: 97, 668: 97, 495: 97, 691: 97, 614: 97, 725: 97, 395: 97, 175: 97, 77: 97, 31: 97, 400: 97, 688: 97, 562: 97, 291: 97, 608: 97, 154: 97, 794: 97, 123: 97, 584: 97, 620: 97, 283: 97, 277: 97, 714: 97, 862: 96, 533: 96, 104: 96, 630: 96, 891: 96, 829: 96, 698: 96, 138: 96, 434: 96, 37: 96, 542: 96, 249: 96, 863: 96, 166: 96, 136: 96, 766: 96, 207: 96, 660: 96, 176: 96, 678: 96, 93: 96, 638: 96, 182: 96, 331: 96, 694: 96, 483: 96, 399: 96, 740: 96, 235: 96, 340: 96, 45: 96, 266: 96, 498: 96, 14: 96, 289: 96, 262: 96, 256: 96, 415: 96, 128: 96, 413: 96, 488: 95, 437: 95, 892: 95, 661: 95, 430: 95, 198: 95, 592: 95, 265: 95, 550: 95, 697: 95, 524: 95, 227: 95, 450: 95, 612: 95, 0: 95, 59: 95, 451: 95, 338: 95, 24: 95, 71: 95, 461: 95, 161: 95, 145: 95, 54: 95, 312: 95, 347: 95, 304: 95, 186: 95, 416: 95, 244: 95, 456: 95, 348: 95, 208: 95, 351: 95, 187: 95, 650: 95, 700: 95, 106: 95, 760: 95, 813: 95, 806: 94, 402: 94, 358: 94, 558: 94, 420: 94, 8: 94, 58: 94, 493: 94, 895: 94, 796: 94, 513: 94, 545: 94, 735: 94, 848: 94, 299: 94, 544: 94, 709: 94, 85: 94, 199: 94, 349: 94, 563: 94, 769: 94, 32: 94, 251: 94, 846: 94, 179: 94, 834: 94, 350: 94, 601: 94, 718: 94, 281: 94, 859: 94, 827: 94, 171: 94, 231: 94, 758: 94, 51: 94, 866: 94, 657: 94, 677: 94, 168: 94, 135: 94, 672: 94, 492: 94, 359: 94, 502: 94, 717: 94, 507: 94, 702: 94, 204: 94, 407: 94, 120: 94, 264: 94, 625: 94, 7: 93, 667: 93, 169: 93, 376: 93, 229: 93, 230: 93, 768: 93, 519: 93, 203: 93, 196: 93, 448: 93, 707: 93, 624: 93, 378: 93, 217: 93, 482: 93, 34: 93, 585: 93, 78: 93, 615: 93, 772: 93, 756: 93, 854: 93, 763: 93, 372: 93, 115: 93, 511: 93, 234: 93, 541: 93, 787: 93, 247: 93, 109: 93, 491: 93, 520: 93, 457: 93, 732: 93, 636: 93, 579: 93, 86: 93, 742: 93, 737: 93, 525: 93, 586: 93, 480: 93, 589: 93, 181: 93, 326: 92, 321: 92, 64: 92, 841: 92, 655: 92, 385: 92, 429: 92, 202: 92, 159: 92, 646: 92, 836: 92, 131: 92, 728: 92, 30: 92, 246: 92, 819: 92, 241: 92, 674: 92, 362: 92, 89: 92, 485: 92, 779: 92, 577: 92, 319: 92, 107: 92, 551: 92, 307: 92, 778: 92, 87: 92, 802: 92, 269: 92, 3: 92, 770: 92, 777: 92, 490: 92, 452: 92, 653: 92, 273: 92, 598: 92, 141: 92, 611: 92, 139: 91, 389: 91, 781: 91, 365: 91, 436: 91, 896: 91, 302: 91, 15: 91, 828: 91, 538: 91, 253: 91, 613: 91, 804: 91, 539: 91, 875: 91, 410: 91, 897: 91, 371: 91, 775: 91, 693: 91, 329: 91, 588: 91, 559: 91, 850: 91, 374: 91, 33: 91, 656: 91, 373: 91, 386: 91, 147: 91, 185: 91, 572: 91, 363: 91, 508: 91, 764: 91, 720: 91, 149: 91, 310: 91, 296: 91, 571: 91, 205: 91, 92: 91, 150: 91, 263: 91, 444: 91, 882: 90, 226: 90, 119: 90, 546: 90, 540: 90, 69: 90, 132: 90, 414: 90, 689: 90, 442: 90, 886: 90, 798: 90, 379: 90, 817: 90, 295: 90, 268: 90, 527: 90, 762: 90, 835: 90, 871: 90, 129: 90, 470: 90, 893: 90, 48: 90, 327: 90, 843: 90, 529: 90, 788: 90, 274: 90, 70: 90, 547: 90, 401: 90, 503: 90, 408: 90, 80: 90, 121: 90, 644: 90, 189: 90, 641: 90, 518: 90, 719: 90, 597: 90, 20: 89, 704: 89, 112: 89, 47: 89, 446: 89, 670: 89, 320: 89, 369: 89, 163: 89, 567: 89, 357: 89, 339: 89, 822: 89, 528: 89, 9: 89, 497: 89, 583: 89, 731: 89, 752: 89, 536: 89, 404: 89, 860: 89, 225: 89, 708: 89, 690: 89, 671: 89, 311: 89, 830: 89, 609: 89, 406: 89, 587: 89, 190: 89, 260: 89, 590: 89, 239: 89, 701: 89, 785: 89, 384: 89, 569: 89, 148: 89, 222: 89, 170: 88, 72: 88, 573: 88, 812: 88, 800: 88, 820: 88, 254: 88, 398: 88, 405: 88, 322: 88, 600: 88, 200: 88, 676: 88, 192: 88, 699: 88, 711: 88, 773: 88, 397: 88, 315: 88, 840: 88, 245: 88, 352: 88, 560: 88, 753: 88, 391: 88, 65: 88, 746: 88, 739: 88, 852: 88, 826: 88, 880: 88, 618: 88, 824: 88, 837: 88, 619: 88, 228: 88, 423: 88, 28: 88, 463: 88, 12: 88, 516: 88, 878: 88, 74: 88, 298: 88, 165: 88, 839: 88, 757: 88, 664: 88, 623: 88, 313: 88, 548: 87, 68: 87, 292: 87, 13: 87, 634: 87, 881: 87, 360: 87, 580: 87, 803: 87, 117: 87, 5: 87, 801: 87, 267: 87, 162: 87, 682: 87, 353: 87, 748: 87, 118: 87, 122: 87, 703: 87, 648: 87, 686: 87, 46: 87, 807: 87, 233: 87, 97: 87, 324: 87, 501: 87, 280: 87, 557: 87, 838: 87, 685: 87, 79: 87, 631: 87, 484: 87, 445: 87, 388: 87, 873: 87, 144: 87, 2: 87, 439: 87, 514: 87, 334: 87, 477: 87, 632: 87, 42: 87, 240: 87, 759: 87, 749: 87, 403: 87, 393: 86, 675: 86, 412: 86, 287: 86, 284: 86, 887: 86, 323: 86, 549: 86, 156: 86, 874: 86, 858: 86, 333: 86, 793: 86, 509: 86, 637: 86, 243: 86, 355: 86, 328: 86, 652: 86, 747: 86, 197: 86, 314: 86, 81: 86, 755: 86, 486: 86, 215: 86, 782: 86, 552: 86, 844: 86, 275: 86, 659: 86, 517: 86, 38: 86, 152: 86, 421: 86, 83: 86, 126: 85, 790: 85, 832: 85, 330: 85, 870: 85, 872: 85, 11: 85, 390: 85, 318: 85, 142: 85, 534: 85, 422: 85, 640: 85, 633: 85, 98: 85, 564: 85, 218: 85, 780: 85, 56: 85, 795: 85, 220: 85, 88: 85, 279: 85, 621: 85, 361: 85, 816: 85, 505: 85, 535: 85, 666: 85, 276: 85, 510: 85, 831: 85, 153: 84, 18: 84, 695: 84, 278: 84, 50: 84, 343: 84, 160: 84, 1: 84, 316: 84, 532: 84, 212: 84, 512: 84, 884: 84, 317: 84, 605: 84, 297: 84, 460: 84, 543: 84, 466: 84, 432: 84, 865: 84, 593: 84, 76: 84, 387: 84, 715: 84, 364: 84, 566: 83, 449: 83, 647: 83, 723: 83, 143: 83, 427: 83, 82: 83, 19: 83, 409: 83, 594: 83, 99: 83, 285: 83, 250: 83, 654: 83, 134: 83, 61: 83, 380: 83, 75: 83, 496: 83, 487: 83, 736: 83, 272: 83, 325: 83, 867: 83, 426: 83, 435: 83, 433: 83, 305: 83, 561: 83, 96: 83, 261: 83, 335: 83, 236: 83, 833: 83, 90: 82, 300: 82, 417: 82, 606: 82, 857: 82, 133: 82, 100: 82, 441: 82, 282: 82, 308: 82, 765: 82, 464: 82, 799: 82, 4: 82, 500: 82, 899: 82, 617: 82, 27: 82, 344: 82, 341: 82, 146: 82, 21: 82, 288: 81, 786: 81, 603: 81, 726: 81, 849: 81, 673: 81, 635: 81, 885: 81, 140: 81, 469: 81, 394: 81, 712: 81, 877: 81, 257: 81, 57: 81, 751: 81, 286: 81, 771: 81, 643: 81, 219: 80, 206: 80, 876: 80, 530: 80, 861: 80, 270: 80, 642: 80, 248: 80, 194: 80, 216: 80, 95: 80, 553: 80, 681: 79, 574: 79, 679: 79, 845: 79, 6: 79, 367: 79, 506: 79, 111: 79, 791: 79, 478: 79, 238: 79, 730: 79, 337: 79, 815: 79, 116: 78, 713: 78, 127: 78, 164: 78, 462: 78, 396: 77, 431: 77, 16: 77, 102: 75, 473: 75, 851: 75, 62: 75, 626: 74, 63: 74, 105: 74, 808: 74, 101: 74, 52: 73, 745: 73, 582: 72, 499: 71, 237: 70, 23: 70, 622: 69, 879: 69, 645: 68}
ff_bus_reqs_count = [ff_bus_utility[key] for key in ff_bus_utility if key is not None]
gc_bus_reqs_count = [gc_bus_utility[key] for key in gc_bus_utility if key is not None]
ob_bus_reqs_count = [96]
# plt.hist(ff_bus_reqs_count)
plt.hist(gc_bus_reqs_count)
plt.show()