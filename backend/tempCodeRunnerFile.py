            if searchMethod == 0:
                print("hey")
                a = []
                result = collection.find({f'{specific_valuee}':{'$regex':f'^{query}'}})

                for doc in result:
                    print(doc)
                    a.append(doc)
                
                print(a)

                return a
            
            elif searchMethod == 1:
                a = []
                print(type(query))
                result = collection.find({specific_valuee : query})
                for doc in result:
                    print(doc)
                    a.append(doc)
                return a