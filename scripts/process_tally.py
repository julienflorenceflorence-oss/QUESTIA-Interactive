import csv
import json
import os
from collections import Counter

# MAPPING BASED ON Questia_Sondage.html
# profil, taille, frustration, ia_integration, squads, interet, pilote, email

def process_csv(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    data = {
        "global": {
            "total_responses": 0,
            "completion_rate": 0,
            "avg_interest_score": 0,
            "pilot_rate": 0,
            "emails_collected": 0
        },
        "acquisition": {},
        "profils": {},
        "tailles": {},
        "frustrations": Counter(),
        "ia_interest": {},
        "squads_avg": 0,
        "pilot_stats": {"Oui": 0, "Non": 0}
    }

    completed_count = 0
    total_interest_score = 0
    total_squads_score = 0
    pilot_yes = 0
    email_count = 0

    with open(input_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data["global"]["total_responses"] += 1
            
            # UTM / Source (Expected from Tally or URL params)
            source = row.get('utm_source', 'direct').lower()
            data["acquisition"][source] = data["acquisition"].get(source, 0) + 1
            
            # Status
            if row.get('status') == 'Completed':
                completed_count += 1
            
            # SECTION A: Profil & Taille
            profil = row.get('profil', 'Inconnu')
            data["profils"][profil] = data["profils"].get(profil, 0) + 1
            
            taille = row.get('taille', 'Inconnu')
            data["tailles"][taille] = data["tailles"].get(taille, 0) + 1
            
            # SECTION B: Frustrations
            frusts = row.get('frustration', '').split(';')
            for f_item in frusts:
                if f_item:
                    data["frustrations"][f_item] += 1
            
            # SECTION C: IA & Squads
            ia = row.get('ia_integration', 'Non spécifié')
            data["ia_interest"][ia] = data["ia_interest"].get(ia, 0) + 1
            
            squads_val = row.get('squads')
            if squads_val:
                total_squads_score += int(squads_val)
            
            # SECTION D: Interet Score
            interet_val = row.get('interet')
            if interet_val:
                total_interest_score += int(interet_val)
            
            # SECTION E: Pilote & Email
            p = row.get('pilote', 'Non')
            data["pilot_stats"][p] = data["pilot_stats"].get(p, 0) + 1
            if p.lower() in ['oui', 'yes']:
                pilot_yes += 1
            
            if row.get('email'):
                email_count += 1

    # Final Calculations
    total = data["global"]["total_responses"]
    if total > 0:
        data["global"]["completion_rate"] = round((completed_count / total) * 100, 1)
        data["global"]["avg_interest_score"] = round(total_interest_score / total, 1)
        data["global"]["pilot_rate"] = round((pilot_yes / total) * 100, 1)
        data["global"]["emails_collected"] = email_count
        data["squads_avg"] = round(total_squads_score / total, 1)

    # Clean Counter for JSON
    data["frustrations"] = dict(data["frustrations"])

    # FIX: Write to .js to bypass CORS issues on local files
    js_content = f"const dashboardData = {json.dumps(data, indent=4, ensure_ascii=False)};"
    with open(output_path.replace('.json', '.js'), 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"Metrics synced with Questia_Sondage.html and saved to {output_path.replace('.json', '.js')}")

if __name__ == "__main__":
    process_csv('QUESTIA/scripts/responses.csv', 'QUESTIA/dashboard/data.js')
