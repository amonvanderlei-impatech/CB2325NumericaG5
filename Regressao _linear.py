def media(dado): #recebe uma lista de inteiros e retorna a sua média
    if len(dado) == 0:
        return KeyError
    else:
        soma = 0

        for i in dado:
            soma += i
        
        return soma/(len(dado))
def regressão_linear(xizes,ypsilons):
    if len(xizes) != len(ypsilons):
        return IndexError
    

    den_beta_chapeu =  -len(xizes)*(media(xizes)*media(xizes))
    num_beta_chapeu =  -len(xizes)*media(xizes)*media(ypsilons)


    for k in range(len(xizes)):

        den_beta_chapeu += xizes[k]*xizes[k]

        num_beta_chapeu += xizes[k]*ypsilons[k] 
    
    beta_chapeu = num_beta_chapeu/den_beta_chapeu

    alpha_chapeu = media(ypsilons) - beta_chapeu*media(xizes)

    return (beta_chapeu,alpha_chapeu)

x = [0,1,2,3,4]
y = [1.1,1.9,3.0,3.9,5.2]
b,a = regressão_linear(x,y)
print(f"y = {b:.2f}x + {a:.2f}")