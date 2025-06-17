Profiling results from first round: 

Date: Tue Jun 17 09:49:13 2025
Profile file: prof.prof
Execution time: 923.878 seconds
Function calls: 44,925,212 total (44,833,626 primitive)

Ordered by: internal time  
List reduced from 10715 to 10 due to restriction <10>  
| #  | Function               | Calls     | Total Time (s) | Per Call (s) | Cumulative Time (s) | File\:Line                                          |
| -- | ---------------------- | --------- | -------------- | ------------ | ------------------- | --------------------------------------------------- |
| 1  | `_convert_encoding`    | 3,434,691 | **430.936**    | \~0.000      | 431.542             | `tokenization_utils_fast.py:282`                    |
| 2  | `encode_batch`         | 69        | **243.652**    | 3.531        | 243.652             | `{method 'encode_batch' of 'tokenizers.Tokenizer'}` |
| 3  | `decompress_and_count` | 1         | **200.232**    | 200.232      | 908.350             | `script.py:8`                                       |
| 4  | `utf_8_decode`         | 1,811,859 | 11.096         | \~0.000      | 11.096              | `{built-in method _codecs.utf_8_decode}`            |
| 5  | `str.count`            | 3,434,710 | 7.300          | \~0.000      | 7.300               | `{method 'count' of 'str'}`                         |
| 6  | `main`                 | 1         | 4.158          | 4.158        | 914.302             | `script.py:44`                                      |
| 7  | `<listcomp>`           | 138       | 3.743          | 0.027        | 3.743               | `tokenization_utils_fast.py:560`                    |
| 8  | `posix.stat`           | 24,737    | 2.778          | \~0.000      | 2.778               | `{built-in method posix.stat}`                      |
| 9  | `batch_encode_plus`    | 69        | 1.935          | 0.028        | 686.054             | `tokenization_utils_base.py:3094`                   |
| 10 | `io.open_code`         | 2,470     | 1.814          | 0.001        | 1.814               | `{built-in method io.open_code}`                    |
