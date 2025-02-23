import openai
import json
from openai import OpenAI

class NameDecoder:
    def __init__(self, batch_size = 20, debug_print = False): 
        self.DEBUG_PRINT = debug_print # prints batches and prompts 
        self.BATCH_SIZE = batch_size   # large batch size: faster with worse results, small batch size: slower with better results and more api calls $ 
        self.API_KEY = self.__get_api_key() 
        self.client = OpenAI(api_key=self.API_KEY)
        self.BASE_PROMPT = self.__get_base_prompt()
    
    def decodeNames(self, product_name_list): 
        name_list = []
        # run in batches of BATCH_SIZE and combine results
        for i in range(0, len(product_name_list), self.BATCH_SIZE):
            batch_list = product_name_list[i:i + self.BATCH_SIZE]
            if self.debug_print:
                print(f"\nCurrent batch{batch_list}")
            
            # build prompt
            complete_prompt: str = self.BASE_PROMPT
            for name in batch_list:
                complete_prompt += "\n"+ name
            if self.debug_print:
                print(f"\nCurrent prompt: {complete_prompt}")
            # get result
            json_response = self.__get_response_json(complete_prompt)
            name_list.append(json.loads(json_response)["grocery_items"])
        return name_list
    
    def __check_cached_names(self):

        pass
        
    def __get_api_key(self):
        with open(".openai_api_key", "r") as file:
            return file.read().strip()
        
    def __get_base_prompt(self):
        with open(".base_prompt", "r") as file:
            return file.read().strip()
        
    def __get_response_json(self, prompt):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]       
        )
        return completion.choices[0].message.content


def main():
    my_decoder = NameDecoder()
    product_list = ["S/MTN.BNLS BREAST", "FZN ORGANIC GREEN BEANS", "Milk Half Gal Almond Unsweeten", "PUB DICED TOMATOES", "PEPPERS GREEN BELL", "BELL PEPPERS RED"]
    decoded_list = my_decoder.decodeNames(product_name_list=product_list)
    print(decoded_list)

    # TODO 
    # dictionary
    # optimize duplicates

if __name__ == "__main__":
    main()


