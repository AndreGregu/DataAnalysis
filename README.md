=== File Summary ===  
Compressed file size:       4,419,747,840 bytes  
Number of lines:            3,434,691  
Number of segments:         3,434,690  
Number of characters:       14,569,246,888  
Number of tokens:           5,045,820,511  

---  

Profiling results from first round: 

Profile file: prof.prof  
Execution time: 923.878 seconds  
Function calls: 44,925,212 total (44,833,626 primitive)  

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


---  

Profiling results from second round: 

Profile file: prof.prof  
Execution time: 714.876 seconds    
Function calls: 41,491,245 function calls (41,399,226  primitive)  

| #  | Function                 | Calls     | Total Time (s) | Per Call (s) | Cumulative Time (s) | File\:Line                                          |
| -- | ------------------------ | --------- | -------------- | ------------ | ------------------- | --------------------------------------------------- |
| 1  | `_convert_encoding`      | 3,434,691 | **246.257**    | \~0.000      | 246.652             | `tokenization_utils_fast.py:282`                    |
| 2  | `encode_batch`           | 69        | **223.164**    | 3.234        | 223.164             | `{method 'encode_batch' of 'tokenizers.Tokenizer'}` |
| 3  | `decompress_and_count`   | 1         | **188.226**    | 188.226      | 687.525             | `script.py:8`                                       |
| 4  | `read` (buffered reader) | 2,480     | 14.693         | 0.006        | 14.693              | `{method 'read' of '_io.BufferedReader'}`           |
| 5  | `utf_8_decode`           | 1,811,859 | 11.123         | \~0.000      | 11.123              | `{built-in method _codecs.utf_8_decode}`            |
| 6  | `str.count`              | 3,434,710 | 7.303          | \~0.000      | 7.303               | `{method 'count' of 'str'}`                         |
| 7  | `posix.stat`             | 24,744    | 2.876          | \~0.000      | 2.876               | `{built-in method posix.stat}`                      |
| 8  | `io.open_code`           | 2,470     | 2.482          | 0.001        | 2.482               | `{built-in method io.open_code}`                    |
| 9  | `<listcomp>`             | 69        | 1.970          | 0.029        | 248.622             | `tokenization_utils_fast.py:538`                    |
| 10 | `from_file`              | 1         | 1.315          | 1.315        | 1.315               | `{built-in method from_file}`                       |
