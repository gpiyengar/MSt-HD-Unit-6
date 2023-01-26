-- Select most recent glucose, HbA1c, LDL, Creatinine, eGFR, ACR for each diabetic patient and convert to SI units
USE synthea;

SELECT 
	o.observation_date, 
    o.patient, 
    o.encounter, 
    o.observation_code, 
    CASE o.observation_code
		WHEN "33914-3" THEN 'Estimated Glomerular Filtration Rate' -- account for obervation name change
        ELSE observation_description
	END AS observation_description,
    CASE o.observation_code
		WHEN "2339-0" THEN ROUND(observation_value * 0.0555, 2) -- blood glucose SI conversion
		WHEN "38483-4" THEN ROUND(observation_value * 88.42, 0)  -- serum creatinine SI conversion
		WHEN "18262-6" THEN ROUND(observation_value * 0.0259, 2)  -- LDL SI conversion
		WHEN "14959-1" THEN ROUND(observation_value * 0.113, 2)  -- AC Ratio SI conversion
        ELSE observation_value
	END AS observation_value,
	CASE o.observation_code
		WHEN "2339-0" THEN "mmol/L"
		WHEN "38483-4" THEN "umol/L"
		WHEN "18262-6" THEN "mmol/L"
		WHEN "14959-1" THEN "mg/mmol"
        WHEN "33914-3" THEN 'mL/min/{1.73_m2}'
        ELSE units
	END AS units
FROM observations o
JOIN conditions c
	USING (patient)
JOIN (
	SELECT 
		patient, 
		MAX(o2.observation_date) as observation_date
	FROM observations o2
		JOIN (
			SELECT 
				encounter, 
                MAX(observation_date) as observation_date
			FROM observations
			WHERE observation_code IN ('2339-0', '4548-4', '18262-6', '38483-4', '33914-3', '14959-1')
			GROUP BY encounter) as o1 on o2.observation_date = o1.observation_date  -- select most recent encounters
	WHERE o2.observation_code IN ('2339-0', '4548-4', '18262-6', '38483-4', '33914-3', '14959-1')
	GROUP BY o2.patient) as o3 on o.observation_date = o3.observation_date -- select most recent encounters per patient
WHERE o.observation_code IN ('2339-0', '4548-4', '18262-6', '38483-4', '33914-3', '14959-1') -- select for glucose, HbA1c, LDL, Creatinine, eGFR, ACR
AND c.condition_code = "44054006"; -- refine to only patients with diagnosis of diabetes