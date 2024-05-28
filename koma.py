angles_koma = [81, 117, 85]
angles_koma.append(360-90-angles_koma[0]-angles_koma[1])
tailles_koma = {'R': [32, 28.7, 9.7], 'T': [31, 27.7, 9.3], 'O': [30, 26.7, 8.8],
                'C': [29, 25.5, 8.3], 'L': [28, 23.5, 8.0], 'P': [27, 22.5, 7.75]}
for s in 'JR FT AO'.split(): tailles_koma[s[0]]=tailles_koma[s[1]]
for km in tailles_koma: tailles_koma[km] = [27.22222222222222*(v/10) for v in tailles_koma[km]]