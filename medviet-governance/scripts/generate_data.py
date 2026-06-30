# -*- coding: utf-8 -*-
import pandas as pd
from faker import Faker
import random
import os

fake = Faker("vi_VN")
Faker.seed(42)

def generate_patients(n=200):
    records = []
    for _ in range(n):
        records.append({
            "patient_id": fake.uuid4(),
            "ho_ten": fake.name(),
            "cccd": f"{random.randint(0,9)}" +
                    "".join([str(random.randint(0,9)) for _ in range(11)]),
            "ngay_sinh": fake.date_of_birth(minimum_age=18, maximum_age=90)
                              .strftime("%d/%m/%Y"),
            "so_dien_thoai": f"0{random.choice([3,5,7,8,9])}" +
                              "".join([str(random.randint(0,9)) for _ in range(8)]),
            "email": fake.email(),
            "dia_chi": fake.address(),
            "benh": random.choice([u"Ti\u1ec3u \u0111\u01b0\u1eddng", u"Huy\u1ebft \u00e1p cao",
                                   u"Tim m\u1ea1ch", u"Kh\u1ecfe m\u1ea1nh"]),
            "ket_qua_xet_nghiem": round(random.uniform(3.5, 12.0), 2),
            "bac_si_phu_trach": fake.name(),
            "ngay_kham": fake.date_this_year().strftime("%d/%m/%Y"),
        })
    return pd.DataFrame(records)

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

df = generate_patients()
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/patients_raw.csv", index=False, encoding="utf-8")
print(f"Generated {len(df)} patient records")
print(df.head(3))