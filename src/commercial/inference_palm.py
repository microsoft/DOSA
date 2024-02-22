from dotenv import load_dotenv
import os
import google.generativeai as palm

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

load_dotenv()


palm.configure(api_key=os.getenv("PALM_API_TOKEN"))


# @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def palm_completion(sys_prompt, inst_prompt):
    try:
        response = palm.chat(context=sys_prompt, temperature=0.1, messages=inst_prompt)
    except Exception as e:
        print(e)
        return "Answer: api failed"
    return response


prompt = "अन्य कई पर्व भी यहाँ होते हैं: जैसे आम महोत्सव, पतंगबाजी महोत्सव, वसंत पंचमी जो वार्षिक होते हैं। एशिया की सबसे बड़ी ऑटो प्रदर्शनी: ऑटो एक्स्पो दिल्ली में द्विवार्षिक आयोजित होती है। प्रगति मैदान में वार्षिक पुस्तक मेला आयोजित होता है। यह विश्व का दूसरा सबसे बड़ा पुस्तक मेला है, जिसमें विश्व के २३ राष्ट्र भाग लेते हैं। दिल्ली को उसकी उच्च पढ़ाकू क्षमता के कारण कभी कभी विश्व की पुस्तक राजधानी भी कहा जाता है। पंजाबी और मुगलई खान पान जैसे कबाब और बिरयानी दिल्ली के कई भागों में प्रसिद्ध हैं। दिल्ली की अत्यधिक मिश्रित जनसंख्या के कारण भारत के विभिन्न भागों के खानपान की झलक मिलती है, जैसे राजस्थानी, महाराष्ट्रियन, बंगाली, हैदराबादी खाना और दक्षिण भारतीय खाने के आइटम जैसे इडली, सांभर, दोसा इत्यादि बहुतायत में मिल जाते हैं। इसके साथ ही स्थानीय खासियत, जैसे चाट इत्यादि भी खूब मिलती है, जिसे लोग चटकारे लगा लगा कर खाते हैं। इनके अलावा यहाँ महाद्वीपीय खाना जैसे इटैलियन और चाइनीज़ खाना भी बहुतायत में उपलब्ध है। इतिहास में दिल्ली उत्तर भारत का एक महत्त्वपूर्ण व्यापार केन्द्र भी रहा है। पुरानी दिल्ली ने अभी भी अपने गलियों में फैले बाज़ारों और पुरानी मुगल धरोहरों में इन व्यापारिक क्षमताओं का इतिहास छुपा कर रखा है। पुराने शहर के बाजारों में हर एक प्रकार का सामान मिलेगा। तेल में डूबे चटपटे आम, नींबू, आदि के अचारों से लेकर मंहगे हीरे जवाहरात, जेवर तक; दुल्हन के अलंकार, कपड़ों के थान, तैयार कपड़े, मसाले, मिठाइयाँ और क्या नहीं?\n    Q: दिल्ली में वार्षिक पुस्तक मेला कहाँ आयोजित किया जाता है ?\n\n    Referring to the passage above, the correct answer to the given question is:"
sys_prompt = """
You are an NLP assistant whose purpose is to solve reading comprehension problems. You will be provided questions on a set of passages and you will need to provide the answer as it appears in the passage. The answer should be in the same language as the question and the passage."""

if __name__ == "__main__":
    output = palm.chat(
        context=sys_prompt,
        temperature=0.1,
        messages=prompt,
    )
    # output = palm.generate_text(
    #     model="models/text-bison-001",
    #     # prompt=prompt
    #     prompt="Can you explain the meaning of the following Persian proverb? Please write the answer in Japanese: Proverb: Na borde ranj ganj moyassar nemishavad",
    # )
    print(output)
