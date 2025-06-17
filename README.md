Profiling results from first round: 

Tue Jun 17 09:49:13 2025    prof.prof

         44925212 function calls (44833626 primitive calls) in 923.878 seconds

   Ordered by: internal time
   List reduced from 10715 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  3434691  430.936    0.000  431.542    0.000 tokenization_utils_fast.py:282(_convert_encoding)
       69  243.652    3.531  243.652    3.531 {method 'encode_batch' of 'tokenizers.Tokenizer' objects}
        1  200.232  200.232  908.350  908.350 script.py:8(decompress_and_count)
  1811859   11.096    0.000   11.096    0.000 {built-in method _codecs.utf_8_decode}
  3434710    7.300    0.000    7.300    0.000 {method 'count' of 'str' objects}
        1    4.158    4.158  914.302  914.302 script.py:44(main)
      138    3.743    0.027    3.743    0.027 tokenization_utils_fast.py:560(<listcomp>)
    24737    2.778    0.000    2.778    0.000 {built-in method posix.stat}
       69    1.935    0.028  686.054    9.943 tokenization_utils_base.py:3094(batch_encode_plus)
     2470    1.814    0.001    1.814    0.001 {built-in method io.open_code}