from 	handle_PCA 				import EMF_PCA_Handle
from 	handle_WordSelector2 	import EMF_WordSelector_Handle2
from 	lib_PCA 				import PREDICTOR, RESPONSE, INDEX
from 	lib_Runner_Model 		import PredictorTransformationKeys, ResponseTransformationKeys # should come from lib_runner_pca?

class EMF_PCA_Runner(object):
	def __init__(self, hndl_DB):
		self._hndl_DB = hndl_DB
		self._hndl_WrdSlct = EMF_WordSelector_Handle2(self._hndl_DB)
		self._resp_words = None
		self._pred_words = None
		self._hndl_PCA = EMF_PCA_Handle()

	def set_model_from_template(self, template):
		# Set Response Ticker in WordSelector
		self._hndl_WrdSlct.resp_data_tickers = template['responseTickers']
		if 'responseTrns' in template:
			self._hndl_WrdSlct.resp_trns_ptrns 	= template['responseTrns']
		else:
			self._hndl_WrdSlct.resp_trns_ptrns 	= ResponseTransformationKeys
		if 'responseKwargs' in template:
			self._hndl_WrdSlct.resp_trns_kwargs 	= template['responseKwargs']
		if 'responseCanPredict' in template:
			self._hndl_WrdSlct.resp_can_predict 	= template['responseCanPredict']
		if 'predictorKwargs' in template:
			self._hndl_WrdSlct.pred_trns_kwargs 	= template['predictorKwargs']
		if 'predictorCriteria' in template:
			predCrit = template['predictorCriteria']
			if 'periodicity' in predCrit:
				self._hndl_WrdSlct.pred_data_periodicity 	= predCrit['periodicity']
			if 'categorical' in predCrit:
				self._hndl_WrdSlct.pred_data_is_categorical 	= predCrit['categorical']
			if 'minDate' in predCrit:
				self._hndl_WrdSlct.pred_data_min_date 		= predCrit['minDate']
			if 'maxDate' in predCrit:
				self._hndl_WrdSlct.pred_data_max_date 		= predCrit['maxDate']
			if 'matchRespPeriodicity' in predCrit:
				raise NotImplementedError
		if 'responseCriteria' in template:
			respCrit = template['responseCriteria']
			if 'periodicity' in respCrit:
				self._hndl_WrdSlct.resp_data_periodicity 	= respCrit['periodicity']
			if 'categorical' in respCrit:
				self._hndl_WrdSlct.resp_data_is_categorical 	= respCrit['categorical']
			if 'minDate' in respCrit:
				self._hndl_WrdSlct.resp_data_min_date 		= respCrit['minDate']
			if 'maxDate' in respCrit:
				self._hndl_WrdSlct.resp_data_max_date 		= respCrit['maxDate']
		if 'predictorTrns' in template:
			self._hndl_WrdSlct.pred_trns_ptrns 	= template['predictorTrns']
		else:
			self._hndl_WrdSlct.pred_trns_ptrns 	= PredictorTransformationKeys

	def add_data(self):
		self._hndl_WrdSlct.select_pred_words_all_tickers()
		self._hndl_WrdSlct.select_resp_words_all_permutations()
		for hndl_Word in self._hndl_WrdSlct.pred_words:
			self._hndl_PCA.add_word(hndl_Word, word_type=PREDICTOR)
		for hndl_Word in self._hndl_WrdSlct.resp_words:
			self._hndl_PCA.add_word(hndl_Word, word_type=RESPONSE)

	def run_PCA(self):
		self._hndl_PCA.run_PCA()

