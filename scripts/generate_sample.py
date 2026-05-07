import csv
import random
from datetime import datetime, timedelta

# Configuration based on Questia_Sondage.html fields
NUM_RESPONSES = 120
SOURCES = ['linkedin', 'instagram', 'facebook', 'email', 'x', 'direct']
PROFILS = ['pedagogique', 'ld', 'independant']
TAILLES = ['minus_50', '50_200', 'plus_1000']
FRUSTRATIONS = ['completion', 'orale', 'roi', 'generique']
IA_INTEREST = ['priorite', 'tester']

def generate_sample_data(file_path):
    with open(file_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'date', 'utm_source', 'status', 
            'profil', 'taille', 
            'frustration', 
            'ia_integration', 'squads', 
            'interet', 'pilote', 'email'
        ])

        for _ in range(NUM_RESPONSES):
            date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S')
            source = random.choice(SOURCES)
            status = 'Completed' if random.random() > 0.1 else 'Partial'
            
            profil = random.choices(PROFILS, weights=[40, 40, 20])[0]
            taille = random.choice(TAILLES)
            
            num_frust = random.randint(1, 4)
            frust = ";".join(random.sample(FRUSTRATIONS, num_frust))
            
            ia = random.choices(IA_INTEREST, weights=[60, 40])[0]
            squads = random.randint(1, 5)
            
            interet = random.randint(1, 10)
            pilote = 'oui' if interet > 6 and random.random() > 0.2 else 'non'
            email = f"lead_{random.randint(100,999)}@domain.com" if pilote == 'oui' else ""
            
            writer.writerow([date, source, status, profil, taille, frust, ia, squads, interet, pilote, email])

if __name__ == "__main__":
    generate_sample_data('QUESTIA/scripts/responses.csv')
    print("Responses sample generated based on HTML fields.")
