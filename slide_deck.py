# from manim import *  

# from manim_slides import Slide

# from slides.evaluation1 import Evaluation1
# from slides.sem_riskman_method import SemRiskmanMethod
# from slides.title import Title
# from slides.sem_motivation import SemMotivation
# from slides.sem_current_practices import SemCurrentPractices
# from slides.sem_enc_rules1 import SemEncRules1
# from slides.sem_enc_rules2 import SemEncRules2
# from slides.sem_enc_rules3 import SemEncRules3
# from slides.sem_enc_rules3 import SemEncRules3
# from slides.sem_graph_encoding import SemGraphEncoding
# from slides.sem_human_readability import SemHumanReadability
# from slides.sem_video import SemVideo
# from slides.sem_riskman_stats import SemRiskmanStats
# from slides.sem_reasoning_validation import SemReasoningValidation
# from slides.sem_more_shacl import SemMoreShacl
# from slides.sem_conclusion import SemConclusion

# class SlideDeck(Slide):
#     def construct(self):
        
#         title = SemTitle(self, show_footer=False) # 0
#         title.pause()
        
#         main_slides = [
#             SemInitial, # 0
#             SemMotivation, # 1
#             SemCurrentPractices, # 2
#             SemRiskmanMethod, #3
#             SemGraphEncoding, # 4
#             # SemEncRules1, # 5
#             SemEncRules2, # 6
#             SemEncRules3, # 7
#             SemReasoningValidation, #8
#             SemMoreShacl, #9
#             SemRiskmanStats, #10
#             SemHumanReadability, # 11
#             SemVideo, # 12
#             SemConclusion, #13
#         ]
        
#         slide_total = len(main_slides)
#         for i, sld in enumerate(main_slides, start=1):
#             inst = sld(self, show_footer=True, slide_no=i, slide_total=slide_total)
#             inst.pause()
