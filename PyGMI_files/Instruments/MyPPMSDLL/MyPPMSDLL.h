#include "extcode.h"
#pragma pack(push)
#pragma pack(1)

#ifdef __cplusplus
extern "C" {
#endif

/*!
 * PPMSGetField
 */
void __cdecl PPMSGetField(char IPAddress[], LVBoolean Remote, 
	int32_t InstrumentType, double *Field, int32_t *FieldStatus, 
	LVBoolean *Errorstatus, int32_t *Errorcode);
/*!
 * PPMSGetTemp
 */
void __cdecl PPMSGetTemp(char IPAddress[], LVBoolean Remote, 
	int32_t InstrumentType, double *Temperature, int32_t *TemperatureStatus, 
	LVBoolean *Errorstatus, int32_t *Errorcode);
/*!
 * PPMSSetField
 */
void __cdecl PPMSSetField(char IPAddress[], LVBoolean Remote, 
	int32_t InstrumentType, double Field, double Rate, int32_t Approach, 
	int32_t Mode, LVBoolean *Errorstatus, int32_t *Errorcode);
/*!
 * PPMSSetTemp
 */
void __cdecl PPMSSetTemp(char IPAddress[], LVBoolean Remote, 
	int32_t InstrumentType, double Temperature, double Rate, int32_t Approach, 
	LVBoolean *Errorstatus, int32_t *Errorcode);
/*!
 * PPMSWaitFor
 */
void __cdecl PPMSWaitFor(char IPAddress[], LVBoolean Remote, 
	int32_t InstrumentType, LVBoolean WaitForTemperature, LVBoolean WaitForField, 
	LVBoolean WaitForChamber, LVBoolean WaitForPosition, LVBoolean *Errorstatus, 
	int32_t *Errorcode);

MgErr __cdecl LVDLLStatus(char *errStr, int errStrLen, void *module);

#ifdef __cplusplus
} // extern "C"
#endif

#pragma pack(pop)

