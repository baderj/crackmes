from noise_overview import ran_values

ASCII_RANGE = [32, 126] 

def generate_len_db(limit):
    """generate a list of mean key lengths for all msg lengths

        Args:
            limit: up to which msg length should the mean be calculated
        Returns:
            a list of mean key lengths, index i corresponds to msg length i
    """
    len_db = []
    noise_values = set()
    mean_off = sum(ASCII_RANGE)/2
    for i in range(0,limit):
        noise_values = ran_values(i)
        mean_val = 0
        for noise in noise_values:
            char = noise + mean_off
            mean_val += len(str(char))
        mean_val *= i
        mean_val /= len(noise_values)
        len_db.append(mean_val)
    return len_db

for i,l in enumerate(generate_len_db(15)):
    print("<tr><td>{}</td><td>{}</td></tr>".format(i, l))

